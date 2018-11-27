# Learning Django Views

**Getting Started**

```
python3 manage.py migrate
python3 manage.py seed
python3 manage.py runserver
```

## Url Patterns

Expected paths:

-   A path named 'create' at the root (an empty pattern), that dispatches your
    short link creation view.
-   A path named 'view' at 'view/\<short_code\>/' that dispatches to your short
    link view view.
-   A path named 'goto' at '\<short_code\>/' that dispatches to your short link
    goto view.

Url patterns example:
https://docs.djangoproject.com/en/2.0/topics/http/urls/#example

## View = HttpRequest -> HttpResponse

HTTP Methods: GET, POST

Django Requests:

-   `request.method` is a `str` that tells you the HTTP method of the request
-   `request.GET` is a `dict` that gives you the GET form data.
-   `request.POST` is a `dict` that gives you the POST form data.

Django Responses:

1.  `render(request, template_path, context)`
    -   `request` is the request
    -   `template_path` is a path (string) into the `./templates` folder.
    -   `context` is a dictionary of data for the template to use
2.  `redirect(url)` or `redirect(path_name, **kwargs)`

## Reading from the Database

I've written the database layer for you.

`from app.models import Link`

Every `Link` has an `.original` and a `.short_code` property.

-   `.original` is the original link
-   `.short_code` is the new short code that the user will provide.

`Link.shorten(url)` is essentially your constructor function. Use it to create a
new short link. If it is given an invalid url, `None` is returned.

`Link.find_by_short_code(short_code)` finds the `Link` corresponding to the
provided short code. If no `Link` corresponds to that short code, `None` is
returned.

## Presenting the Front End

I've done this part as well.

There are two templates for you to use: `app/create.html` and `app/view.html`.

`app/create.html` expects `invalid_url` to be either `True` or `False`.

`app/view.html` expects `link` to be a `Link` or `None`.

# You will know you are done when...

1.  You can create a new short link.
2.  View the original url from that short link.
3.  Use the service to go to the original url when given a short link.
4.  **You pass all the tests**
