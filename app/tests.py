import django.test
from django.urls import reverse, resolve
from django.urls.exceptions import Resolver404, NoReverseMatch
from app.models import Link


class TestCase(django.test.TestCase):
    def assertResolvesTo(self, url, view_name, kwargs=None):
        kwargs = kwargs or {}
        try:
            match = resolve(url)
        except Resolver404:
            raise AssertionError(
                f'{url} didn\'t resolve to a view at all!\n\n'
                f'You expected it to resolve to {view_name} with kwargs={kwargs}.\n\n'
                'Have you added a path to your urlpatterns for it?\n'
                'Are all of the necessary url parameters in place?') from None
        else:
            self.assertEqual(
                match.view_name, view_name,
                f'{url} match to {match.view_name} instead of {view_name}!')
            self.assertEqual(
                match.kwargs, kwargs,
                f'{url} match with kwargs {match.kwargs} instead of {kwargs}')

    def assertRedirectsTo(self, response, view_name, kwargs=None):
        try:
            match = reverse(view_name, kwargs=kwargs)
        except NoReverseMatch:
            raise AssertionError(
                'Unable to determine path for the expected view\n'
                f'{view_name} with {kwargs}\n\n'
                f'Have you added a path named {view_name} to your urlpatterns?\n'
                'Does it have the appropriate url parameters?') from None
        else:
            self.assertRedirects(
                response, match, fetch_redirect_response=False)


class TestCreateView(TestCase):
    def test_step1_root_resolves_to_app_create(self):
        'The path for root (the empty path) should resolve to a view named app:create'
        self.assertResolvesTo('/', 'app:create')

    def test_step2_get_app_create_renders_app_create_html(self):
        'Making a GET request to app:create should render with app/create.html'
        self.client.get(reverse('app:create'))
        self.assertTemplateUsed('app/create.html')

    def test_step3_post_app_create_with_valid_url_creates_link(self):
        'Make a POST request to app:create with a valid url should create a new Link'
        self.client.post(
            reverse('app:create'),
            {'url': 'https://www.basecampcodingacademy.org'},
        )

        self.assertTrue(
            Link.objects.filter(
                original='https://www.basecampcodingacademy.org').exists())

    def test_step4_post_app_create_with_valid_url_redirects_to_app_show(self):
        '''Making a POST request to app:create with a valid url
        should redirect to app:show for the newly created link.'''
        response = self.client.post(
            reverse('app:create'),
            {'url': 'https://www.basecampcodingacademy.org'})

        link = Link.objects.get(
            original='https://www.basecampcodingacademy.org')

        self.assertRedirectsTo(
            response,
            'app:show',
            kwargs={'short_code': link.id},
        )

    def test_step5_post_app_create_with_invalid_url_renders_app_create_invalid_url(
            self):
        '''POSTing to app:create with an invalid url
        should render app/create.html with invalid_url as True'''
        response = self.client.post(
            reverse('app:create'), {'url': 'not a valid url'})

        self.assertTemplateUsed(response, 'app/create.html')
        self.assertTrue(response.context.get('invalid_url'))

    def test_step6_post_app_create_with_invalid_url_response_with_422(self):
        'POSTing to app:create with an invalid url should respond with UNPROCESSABLE_ENTITY 422'
        response = self.client.post(
            reverse('app:create'),
            {'url': 'not a valid url'},
        )

        self.assertEqual(response.status_code, 422)


class TestShowView(TestCase):
    def test_step1_link_shortcode_resolves_to_app_show(self):
        '''The path for /link/1/ should resolve to app:show
        with an argument `short_code` of 1.'''
        self.assertResolvesTo(
            '/link/1/', 'app:show', kwargs={'short_code': '1'})

    def test_step2_get_existing_link_renders_app_show_with_link(self):
        '''app:show with the short_code for an existing link
        renders app/show.html with the short_code's link provided in
        the context.'''
        l = Link.shorten('https://www.basecampcodingacademy.org')

        response = self.client.get(
            reverse('app:show', kwargs={'short_code': l.short_code}), )

        self.assertTemplateUsed(response, 'app/show.html')
        self.assertEqual(response.context.get('link'), l)

    def test_step3_get_nonexistent_link_renders_app_show_with_None(self):
        '''If the link doesn't exist, the app:show should render app/show.html
        with `None` as "link" in the context.'''
        response = self.client.get(
            reverse('app:show', kwargs={'short_code': 1}))

        self.assertTemplateUsed(response, 'app/show.html')
        self.assertEqual(response.context.get('link'), None)


class TestGotoView(TestCase):
    def test_step1_short_code_resolves_to_app_goto(self):
        '''The path for /1/' should resolve to app:goto
        with a `short_code` argument of 1.'''
        self.assertResolvesTo('/1/', 'app:goto', kwargs={'short_code': '1'})

    def test_step2_app_goto_with_existing_link_redirects_to_link_original(
            self):
        'app:goto should redirect to short_code\'s link\'s original url'
        l = Link.shorten('https://www.basecampcodingacademy.org')

        response = self.client.get(
            reverse('app:goto', kwargs={'short_code': l.short_code}))

        self.assertRedirects(
            response, l.original, fetch_redirect_response=False)

    def test_step3_app_goto_with_nonexistent_link_redirects_to_app_create(
            self):
        'If short_code doesn\'t exist, it should redirect to app:create'
        response = self.client.get(
            reverse('app:goto', kwargs={'short_code': 1}))

        self.assertRedirectsTo(response, 'app:create')
