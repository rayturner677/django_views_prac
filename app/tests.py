from django.test import TestCase
from django.urls import reverse
from app.models import Link


class TestCreateView(TestCase):
    def test_root_resolves_to_app_create(self):
        'The urlpattern for root should resolve to a view named app:create'
        response = self.client.get('/')
        self.assertEqual(response.resolver_match.view_name, 'app:create')

    def test_get_app_create_renders_app_create_html(self):
        'Making a GET request to app:create should render with app/create.html'
        response = self.client.get(reverse('app:create'))
        self.assertTemplateUsed('app/create.html')

    def test_post_app_create_with_valid_url_creates_link(self):
        'Make a POST request to app:create with a valid url creates a new Link'
        response = self.client.post(
            reverse('app:create'),
            {'url': 'https://www.basecampcodingacademy.org'})

        self.assertTrue(
            Link.objects.filter(
                original='https://www.basecampcodingacademy.org').exists())

    def test_post_app_create_with_valid_url_redirects_to_app_view(self):
        '''Making a POST request to app:create with a valid url
        should redirect to app:view the newly created link.'''
        response = self.client.post(
            reverse('app:create'),
            {'url': 'https://www.basecampcodingacademy.org'})

        link = Link.objects.get(
            original='https://www.basecampcodingacademy.org')

        self.assertRedirects(response,
                             reverse(
                                 'app:view', kwargs={'short_code': link.id}))

    def test_post_app_create_with_invalid_url_response_with_422(self):
        '''Posting to app:create with an invalid url
        should respond with UNPROCESSABLE_ENTITY 403'''
        response = self.client.post(
            reverse('app:create'), {'url': 'not a valid url'})

        self.assertEqual(response.status_code, 422)

    def test_post_app_create_with_invalid_url_renders_app_create_invalid_url(
            self):
        '''Posting to app:create with an invalid url
        should render app/create.html with invalid_url as True'''
        response = self.client.post(
            reverse('app:create'), {'url': 'not a valid url'})

        self.assertTemplateUsed(response, 'app/create.html')
        self.assertTrue(response.context.get('invalid_url'))


class TestViewView(TestCase):
    def test_view_code_resolves_to_app_view(self):
        response = self.client.get('/view/1/')

        self.assertEqual(response.resolver_match.view_name, 'app:view')
        self.assertEqual(response.resolver_match.kwargs['short_code'], '1')

    def test_get_existing_link_renders_app_view_with_link(self):
        l = Link.shorten('https://www.basecampcodingacademy.org')

        response = self.client.get(
            reverse('app:view', kwargs={'short_code': l.short_code}))

        self.assertTemplateUsed(response, 'app/view.html')
        self.assertEqual(response.context.get('link'), l)

    def test_get_nonexistent_link_renders_app_view_with_None(self):
        response = self.client.get(
            reverse('app:view', kwargs={'short_code': 1}))

        self.assertTemplateUsed(response, 'app/view.html')
        self.assertEqual(response.context.get('link'), None)


class TestGotoView(TestCase):
    def test_short_code_resolves_to_app_goto(self):
        response = self.client.get('/1/')

        self.assertEqual(response.resolver_match.view_name, 'app:goto')

    def test_app_goto_with_existing_link_redirects_to_link_original(self):
        l = Link.shorten('https://www.basecampcodingacademy.org')

        response = self.client.get(
            reverse('app:goto', kwargs={'short_code': l.short_code}))

        self.assertRedirects(
            response, l.original, fetch_redirect_response=False)

    def test_app_goto_with_nonexistent_link_redirects_to_app_create(self):
        response = self.client.get(
            reverse('app:goto', kwargs={'short_code': 1}))

        self.assertRedirects(response, reverse('app:create'))
