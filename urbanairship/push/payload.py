# coding=utf-8
import re
import sys
import collections
# Python coarse version differentiation
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# Set version string type
if PY3:
    string_type = str
elif PY2:
    string_type = basestring

# Valid autobadge values: auto, +N, -N
VALID_AUTOBADGE = re.compile(r'^(auto|[+-][\d]+)$')
VALID_ANDROID_CATEGORIES = [
    "alarm", "call", "email", "err", "event", "msg", "promo",
    "recommendation", "service", "social", "status", "sys", "transport"
]
VALID_ICON_COLOR = re.compile(r'^#[0-9a-f]{6}$')


def notification(alert=None, ios=None, android=None, amazon=None,
                 web=None, wns=None, actions=None, interactive=None,
                 in_app=None, open_platform=None):
    """Create a notification payload.

    :keyword alert: A simple text alert, applicable for all platforms.
    :keyword ios: An iOS platform override, as generated by :py:func:`ios`.
    :keyword android: An Android platform override, as generated by
        :py:func:`android`.
    :keyword amazon: An Amazon platform override, as generated by
        :py:func:`amazon`.
    :keyword web: A web platform override, as generated by :py:func:`web`.
    :keyword wns: A WNS platform override, as generated by :py:func:`wns`.
    :keyword actions: Used to perform a defined task.
    :keyword interactive: A dictionary with two attributes -- "type" and
        "button_actions", as generated by :py:func:`interactive`.
    :keyword open_platform: A dictionary with open platform name keys, and
        open platform overrides, as generated by :py:func:`open_platform`.

    """
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if actions is not None:
        payload['actions'] = actions
    if ios is not None:
        payload['ios'] = ios
    if android is not None:
        payload['android'] = android
    if amazon is not None:
        payload['amazon'] = amazon
    if web is not None:
        payload['web'] = web
    if wns is not None:
        payload['wns'] = wns
    if interactive is not None:
        payload['interactive'] = interactive
    if in_app is not None:
        payload['in_app'] = in_app
    if open_platform is not None:
        for platform, overrides in open_platform.items():
            payload['open::' + platform] = overrides
    if not payload:
        raise ValueError('Notification body may not be empty')
    return payload


def ios(alert=None, badge=None, sound=None, content_available=False,
        extra=None, expiry=None, interactive=None, category=None, title=None,
        mutable_content=None, subtitle=None, media_attachment=None,
        priority=None, collapse_id=None):
    """iOS/APNS specific platform override payload.

    :keyword alert: iOS format alert, as either a string or dictionary.
    :keyword badge: An integer badge value or an *autobadge* string.
    :keyword sound: The name of a sound file to play. Must be a string.
    :keyword content_available: If True, pass on the content_available command
        for Newsstand iOS applications.
    :keyword extra: A set of key/value pairs to include in the push payload
        sent to the device.
    :keyword expiry: An integer or time set in UTC as a string
    :keyword interactive: A dictionary with two attributes -- "type" and
        "button_actions", as generated by :py:func:`interactive`.
    :keyword category: A keyword used to categorize the notification. Must be
        a string
    :keyword title: Sets the title of the notification for Apple Watch. Must
        be a string
    :keyword mutable_content: Optional, a boolean. Defaults to false.
        When set to true, content may be modified by an extension.
        This flag will be automatically set to true if there is a
        media_attachment in the payload. iOS 10 or above.
    :keyword subtitle: Optional, a string that will display below the title of
        the notification.
        This is provided as a convenience for setting the subtitle in the alert
        JSON object.
        If a subtitle is also defined in the alert JSON object, this value is
        ignored. iOS 10 or above.
    :keyword media_attachment: Optional, a dictionary object `Media Attachment
        <https://docs.urbanairship.com/api/ua/#media-attachment>`_.
        Specifies a media attachment to be handled by the UA Media Attachment
        Extension.
    :keyword collapse_id: Optional, a string. When there is a newer message
        that renders an older, related message irrelevant to the client app,
        the new message replaces the older message with the same collapse_id.
        Similar to the GCM collapse_key. The value of this key must not exceed
        64 bytes. iOS 10 or above.

    >>> ios(alert='Hello!', sound='cat.caf',
    ...     extra={'articleid': '12345'}) # doctest: +SKIP
    {'sound': 'cat.caf', 'extra': {'articleid': '12345'}, 'alert': 'Hello!'}

    """
    payload = {}
    if alert is not None:
        if not (isinstance(alert, (string_type, dict))):
            raise ValueError('iOS alert must be a string or dictionary')
        payload['alert'] = alert
    if badge is not None:
        if not (isinstance(badge, (string_type, int))):
            raise ValueError('iOS badge must be an integer or string')
        if isinstance(badge, string_type) and not VALID_AUTOBADGE.match(badge):
            raise ValueError('Invalid iOS autobadge value')
        payload['badge'] = badge
    if sound is not None:
        payload['sound'] = sound
    if content_available:
        payload['content-available'] = 1
    if extra is not None:
        payload['extra'] = extra
    if expiry is not None:
        if not (isinstance(expiry, (string_type, int))):
            raise ValueError('iOS expiry must be an integer or string')
        payload['expiry'] = expiry
    if interactive is not None:
        payload['interactive'] = interactive
    if category is not None:
        if not (isinstance(category, string_type)):
            raise ValueError('iOS category must be a string')
        payload['category'] = category
    if title is not None:
        if not (isinstance(title, string_type)):
            raise ValueError('iOS title must be a string')
        payload['title'] = title
    if mutable_content is not None:
        payload['mutable_content'] = mutable_content
    if subtitle is not None:
        payload['subtitle'] = subtitle
    if media_attachment is not None:
        payload['media_attachment'] = media_attachment
    if priority is not None:
        if priority not in {10, 5}:
            raise ValueError('iOS priority must be set to one of 5 or 10.')
        payload['priority'] = priority
    if collapse_id is not None:
        if not (isinstance(collapse_id, string_type)):
            raise ValueError('iOS collapse_id must be a string')
        payload['collapse_id'] = collapse_id

    return payload


def android(alert=None, collapse_key=None, time_to_live=None,
            delay_while_idle=False, extra=None, interactive=None,
            local_only=None, wearable=None, delivery_priority=None,
            style=None, title=None, summary=None, sound=None, priority=None,
            category=None, visibility=None, public_notification=None,
            notification_tag=None, notification_channel=None, icon=None,
            icon_color=None):
    """Android specific platform override payload.

    All keyword arguments are optional.

    :keyword alert: String alert text.
    :keyword collapse_key: String
    :keyword time_to_live: Integer
    :keyword delay_while_idle: Boolean
    :keyword extra: A set of key/value pairs to include in the push payload
        sent to the device. All values must be strings.
    :keyword interactive: A dictionary with two attributes -- "type" and
        "button_actions", as generated by :py:func:`interactive`.
    :keyword local_only: Optional value for not showing the notification on
        wearable devices. Defaults to False.
    :keyword wearable: Optional object to define a wearable notification
        with the following optional fields: background_image, extra_pages, and
        interactive.
    :keyword delivery_priority: Optional string of either 'high' or 'normal'.
        Sets the GCM priority.
    :keyword style: Optional object. Defines an advanced style.
    :keyword title: Optional string. Represents the title of the notification.
    :keyword summary: Optional string. Represents a summary of the
        notification.
    :keyword sound: Optional string. Represents a sound file name included
        in the app resources.
    :keyword priority: Optional integer between -2 and 2. An Android L feature
        that determines location sort order.
    :keyword category: Optional string. An Android category.
    :keyword visibility: Optional integer between -1 and 1.
    :keyword public_notification: Optional object. A notification to show on
        the lock screen instead instead of the redacted one.
    :keyword notification_tag: Optional string. A string identifier used to
        replace an existing notification in the notification drawer.
    :keyword notification_channel: Optional string.  An identifier of a
        notification channel predefined by the application.
    :keyword icon: Optional string. The name of a drawable in the
        application’s resource directory.
    :keyword icon_color: Optional. A string in the format of #rrggbb that
        defines the notification accent color.

    See
    `GCM Advanced Topics <http://developer.android.com/google/gcm/adv.html>`_
    for details on ``collapse_key``, ``time_to_live``, and
    ``delay_while_idle``.

    >>> android(alert='Hello!', extra={'articleid': '12345'}) # doctest: +SKIP
    {'extra': {'articleid': '12345'}, 'alert': 'Hello!'}

    """
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if collapse_key is not None:
        payload['collapse_key'] = collapse_key
    if time_to_live is not None:
        payload['time_to_live'] = time_to_live
        if not (isinstance(time_to_live, (string_type, int))):
            raise ValueError('Android time_to_live value must be an '
                             'integer or time set in UTC as a string')
    if delay_while_idle:
        payload['delay_while_idle'] = True
    if extra is not None:
        payload['extra'] = extra
    if interactive is not None:
        payload['interactive'] = interactive
    if local_only is not None:
        if not (isinstance(local_only, bool)):
            raise ValueError('Android local_only must be a boolean value')
        payload['local_only'] = local_only
    if wearable is not None:
        if not (isinstance(wearable, dict)):
            raise ValueError('Android wearable must be a dictionary')
        payload['wearable'] = wearable
    if delivery_priority is not None:
        if delivery_priority not in {'high', 'normal'}:
            raise ValueError(
                "delivery_priority must be set to one of 'high' or 'normal'."
            )
        payload["delivery_priority"] = delivery_priority
    if style is not None:
        payload['style'] = style
    if title is not None:
        payload['title'] = title
    if summary is not None:
        payload['summary'] = summary
    if sound is not None:
        payload['sound'] = sound
    if priority is not None:
        if priority not in range(-2, 3):
            raise ValueError(
                'priority must be set to one of {}.'.format(
                    ', '.join([str(i) for i in range(-2, 3)])
                )
            )
        payload['priority'] = priority
    if category is not None:
        if category not in VALID_ANDROID_CATEGORIES:
            raise ValueError(
                'category must be set to one of {}.'.format(
                    ', '.join(VALID_ANDROID_CATEGORIES)
                )
            )
        payload['category'] = category
    if visibility is not None:
        if visibility not in range(-1, 2):
            raise ValueError(
                'visibility must be set to one of {}.'.format(
                    ', '.join([str(i) for i in range(-1, 2)])
                )
            )
        payload['visibility'] = visibility
    if public_notification is not None:
        payload['public_notification'] = public_notification
    if notification_tag is not None:
        payload['notification_tag'] = notification_tag
    if notification_channel is not None:
        payload['notification_channel'] = notification_channel
    if icon is not None:
        payload['icon'] = icon
    if icon_color is not None:
        if (isinstance(icon_color, string_type) and not
                VALID_ICON_COLOR.match(icon_color)):
            raise ValueError('icon_color must be in format #rrggbb')
        payload['icon_color'] = icon_color

    return payload


def amazon(alert=None, consolidation_key=None, expires_after=None, extra=None,
           title=None, summary=None, interactive=None, style=None, sound=None):
    """Amazon specific platform override payload.

    All keyword arguments are optional.

    :keyword alert: String alert text.
    :keyword consolidation_key: String
    :keyword expires_after: Integer or UTC time (string)
    :keyword extra: A set of key/value pairs to include in the push payload
        sent to the device. All values must be strings.
    :keyword title: String
    :keyword summary: String
    :keyword interactive: A dictionary with two attributes -- "type" and
        "button_actions", as generated by :py:func:`interactive`.


    >>> amazon(alert='Hello!', title='My Title',
    ...     extra={'articleid': '12345'}) # doctest: +SKIP
    {'title': 'My Title', 'extra': {'articleid': '12345'}, 'alert': 'Hello!'}

    """
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if consolidation_key is not None:
        payload['consolidation_key'] = consolidation_key
    if expires_after is not None:
        payload['expires_after'] = expires_after
        if not (isinstance(expires_after, (string_type, int))):
            raise ValueError('Amazon time_to_live value must be an '
                             'integer or time set in UTC as a string')
    if extra is not None:
        payload['extra'] = extra
    if title is not None:
        payload['title'] = title
    if summary is not None:
        payload['summary'] = summary
    if interactive is not None:
        payload['interactive'] = interactive
    if style is not None:
        payload['style'] = style
    if sound is not None:
        payload['sound'] = sound
    return payload


def web(alert=None, extra=None, icon=None, title=None, interactive=None,
        time_to_live=None, require_interaction=None):
    """Web specific platform override payload.

    All keyword arguments are optional

    :keyword alert: An optional string alert text.
    :keyword extra: An optional set of key/value pairs to include in the push
        payload sent to the device.
    :keyword icon: An optional JSON dictionary of string key and value pairs.
        Key must be 'url' and value, an HTTPS URL to the icon resource.
    :keyword title: Optional string. Represents the title of the notification.
    :keyword interactive: An optional dictionary with two attributes --
        ``type`` and ``button_actions``, as generated by :py:func:`interactive`
    :keyword time_to_live: An optional integer or time set in UTC as a string
    :keyword require_interaction: An optional boolean value that requires user
        interaction on the notification before it is dismissed.


    >>> web(extra={'articleid': '12345'},
    ...    icon={'url': 'https://example.com/icon.png'},
    ...    title='This is a title!') # doctest: +SKIP
    {'title': 'This is a title!', 'extra': {'articleid': '12345'},
     'icon': {'url': 'https://example.com/icon.png'}, 'alert': 'Hello!'}

    """
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if extra is not None:
        payload['extra'] = extra
    if icon is not None:                # todo: possibly set 'url' key
        payload['icon'] = icon
        if not isinstance(icon, dict):
            raise TypeError('icon must be a dictionary')
    if title is not None:
        payload['title'] = title
    if interactive is not None:
        payload['interactive'] = interactive
    if time_to_live is not None:
        if not (isinstance(time_to_live, (string_type, int))):
            raise ValueError('Web time_to_live must be an integer or string')
        payload['time_to_live'] = time_to_live
    if require_interaction is not None:
        if not (isinstance(require_interaction, (bool))):
            raise ValueError('require_interaction must be boolean type')
        payload['require_interaction'] = require_interaction
    return payload


def open_platform(alert=None, title=None, extra=None, summary=None,
                  media_attachment=None, interactive=None):
    """Open platform specific override payload.

    All keyword arguments are optional.

    :keyword alert: String alert text.
    :keyword title: String, represents the title of the notification.
    :keyword summary: A string value for providing a content summary.
    :keyword media_attachment: A URI for an image or video somewhere on the
        internet.
    :keyword extra: A set of key/value pairs to include in the push payload
        sent to the device.
    :keyword interactive: An interactive payload override, as generated by
        :py:func:`interactive`. Included button actions must be of type
        ``add_tag``, ``remove tag``, ``app_defined``, or ``open`` with subtype
        ``url``.

    >>> sms_overrides = open_platform(
    ...    alert='Hello!',
    ...    title='See my new homepage!',
    ...    summary='A longer summary of some content',
    ...    media_attachment='https://example.com/cat_standing_up.jpeg',
    ...    extra={'some_info': 'for sms only'},
    ...    interactive=interactive(
    ...            type='ua_yes_no_foreground',
    ...            button_actions={
    ...                'yes': actions(open_={
    ...                    'type':'url',
    ...                    'content':'https://www.urbanairship.com'
    ...                    }),
    ...                'no': actions(app_defined={'foo': 'bar'})
    ...            }
    ...        ) # doctest: +SKIP
    {'alert': 'Hello!', 'title': 'See my new homepage!', 'summary':
    'A longer summary of some content', 'media_attachment':
    'https://example.com/cat_standing_up.jpeg', 'extra': {'some_info':
    'for sms only'}, 'interactive': {'type': 'ua_yes_no_foreground',
    'button_actions': { 'yes': {'open': {'type': 'url', 'content':
    'http://www.urbanairship.com'}}, 'no': {'app_defined': {'foo': 'bar'}}}}}

    >>> notification(open_platform={'sms': sms_overrides}) # doctest: +SKIP

    """
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if title is not None:
        payload['title'] = title
    if extra is not None:
        payload['extra'] = extra
    if summary is not None:
        payload['summary'] = summary
    if media_attachment is not None:
        payload['media_attachment'] = media_attachment
    if interactive is not None:
        payload['interactive'] = interactive
    return payload


def wns_payload(alert=None, toast=None, tile=None, badge=None):
    """WNS specific platform override payload.

    Must include exactly one of ``alert``, ``toast``, ``tile``, or ``badge``.

    """
    if sum(1 for x in (alert, toast, tile, badge) if x) != 1:
        raise ValueError('WNS payload must have one notification type.')
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if toast is not None:
        payload['toast'] = toast
    if tile is not None:
        payload['tile'] = tile
    if badge is not None:
        payload['badge'] = badge
    return payload


def message(title, body, content_type=None, content_encoding=None,
            extra=None, expiry=None, icons=None, options=None,
            campaigns=None):
    """Rich push message payload creation.

    :param title: Required, string
    :param body: Required, string
    :keyword content_type: Optional, MIME type of the body
    :keyword content_encoding: Optional, encoding of the data in body,
        e.g. ``utf-8``.
    :keyword extra: Optional, dictionary of string values.
    :keyword expiry: time when message will delete from Inbox
        (UTC time or in seconds)
    :keyword icons: Optional JSON dictionary of string key and value
        pairs. Values must be URIs or URLs to the icon resources
    :keyword options: Optional JSON dictionary of key and value pairs
        specifying non-payload options

    """
    payload = {
        'title': title,
        'body': body,
    }
    if content_type is not None:
        payload['content_type'] = content_type
    if content_encoding is not None:
        payload['content_encoding'] = content_encoding
    if extra is not None:
        payload['extra'] = extra
    if expiry is not None:
        payload['expiry'] = expiry
        if not (isinstance(expiry, (string_type, int))):
            raise ValueError('Expiry value must be an '
                             'integer or time set in UTC as a string')
    if icons is not None:
        if not isinstance(icons, dict):
            raise TypeError('icons must be a dictionary')
        payload['icons'] = icons
    if options is not None:
        if not isinstance(options, dict):
            raise TypeError('options must be a dictionary')
        payload['options'] = options
    if campaigns is not None:
        if not isinstance(campaigns, dict):
            raise TypeError('campaigns must be a dictionary')
        payload['campaigns'] = campaigns

    return payload


def in_app(alert, display_type, expiry=None, display=None,
           actions=None, interactive=None, extra=None):
    """In-App push message payload creation.

    :param alert: Required, string
    :param display_type: Required, String. List of valid display_type_
        attributes.
    :keyword expiry: Optional, String specifying an expiry value.
    :keyword display: Optional, A dictionary specifying the display_
        appearance of the in-app message.
    :keyword actions: Optional, Used to perform a defined task.
    :keyword interactive: Optional, A dictionary with two attributes –
        "type" and "button_actions", as generated by interactive().
    :keyword extra: Optional, Object.

    .. _display: https://docs.urbanairship.com/api/ua.html#display-object
    .. _display_type: https://docs.urbanairship.com/api/ua.html#in-app-message

    """

    payload = {}

    payload['alert'] = alert
    payload['display_type'] = display_type

    if expiry is not None:
        payload['expiry'] = expiry
    if display is not None:
        payload['display'] = display
    if actions is not None:
        payload['actions'] = actions
    if interactive is not None:
        payload['interactive'] = interactive
    if extra is not None:
        extra['extra'] = extra

    return payload


def device_types(*types):
    """Create a device type specifier.

    >>> device_types('ios', 'wns')
    ['ios', 'wns']
    >>> device_types('ios', 'symbian')
    Traceback (most recent call last):
        ...
    ValueError: Invalid device type 'symbian'

    """
    if len(types) == 1 and types[0] == 'all':
        return 'all'
    for t in types:
        is_open = isinstance(t, string_type) and t.startswith('open::')
        if t not in ('ios', 'android', 'amazon', 'wns', 'web') and not is_open:
            raise ValueError("Invalid device type '%s'" % t)
    return [t for t in types]


def options(expiry=None):
    """Options payload creation.

    :keyword expiry: time at which push will no longer be sent.
        Int or UTC time

    """
    payload = {}
    if expiry is not None:
        payload['expiry'] = expiry
    if not (isinstance(expiry, (string_type, int))):
        raise ValueError('Expiry value must be an '
                         'integer or time set in UTC as a string')
    return payload


def campaigns(categories=None):
    """Campaigns payload creation.

    >>> campaigns(categories=['kittens', 'tacos', 'horse_racing'])
    {'categories': ['kittens', 'tacos', 'horse_racing']}

    """
    payload = {}
    if categories is not None:
        if not isinstance(categories, collections.Sequence):
            raise TypeError('categories must be a string or list of strings')
        if isinstance(categories, list):
            if not categories or len(categories) > 10:
                raise ValueError('Categories list must '
                                 'contain between 1 and 10 items')
        if isinstance(categories, string_type):
            categories = [categories]

        for c in categories:
            if not (isinstance(c, string_type)):
                raise ValueError("Invalid category type '%s'" % c)
            if not len(c) or len(c) > 64:
                raise ValueError("Invalid category name '%s'" % c)
        payload['categories'] = [c for c in categories]
    return payload


def actions(add_tag=None, remove_tag=None,
            open_=None, share=None, app_defined=None):
    """Actions payload creation.

    :keyword add_tag: Adds a tag to the device. Expects a
        string or a list of strings.
    :keyword remove_tag: Removes a tag from the device. Expects
        a string or a list of strings.
    :keyword open_: Opens type url, deep_link or landing_page. Expects a
        dictionary with "type" and "content".
        See API docs for more information.
    :keyword share: Sends a share notification. Expects a string.
    :keyword app_defined: Sends application defined actions. Expects
        a dictionary.

    >>> actions(add_tag='new_tag', remove_tag='old_tag',
    ...     open_={'type': 'url',
    ...         'content': 'http://www.urbanairship.com'}) # doctest: +SKIP
    {'open': {'type': 'url', 'content': 'http://www.urbanairship.com},
     'add_tag': 'new_tag', 'remove_tag': 'old_tag'}

    """
    payload = {}
    if add_tag is not None:
        if not (isinstance(add_tag, (collections.Sequence))):
            raise TypeError('add_tag must be a string or a list of strings')
        if isinstance(add_tag, list) and not add_tag:
            raise ValueError('add_tag list cannot be empty')
        payload['add_tag'] = add_tag
    if remove_tag is not None:
        if not (isinstance(remove_tag, (collections.Sequence))):
            raise TypeError('remove_tag must be a string or a list of strings')
        if isinstance(remove_tag, list) and not remove_tag:
            raise ValueError('remove_tag list cannot be empty')
        payload['remove_tag'] = remove_tag
    if open_ is not None:
        if not (isinstance(open_, dict)):
            raise TypeError('open_ must be a dictionary')
        payload['open'] = open_
    if share is not None:
        if not (isinstance(share, string_type)):
            raise TypeError('share must be a string')
        payload['share'] = share
    if app_defined is not None:
        if not (isinstance(app_defined, dict)):
            raise TypeError('app_defined must be a dictionary')
        payload['app_defined'] = app_defined
    return payload


def interactive(type=None, button_actions=None):
    """Interactive payload creation.
    :keyword type: The name of one of the predefined interactive notifications
    or a custom defined interactive notification. Expects a string.
    :keyword button_actions: A button_actions object that maps button IDs to
    valid action objects. Expects a dictionary.
    """

    payload = {}
    if type is not None:
        payload['type'] = type
        if button_actions is not None:
            if not isinstance(button_actions, dict):
                raise TypeError("'button_actions' must be a dictionary")
            payload['button_actions'] = button_actions
    else:
        raise AttributeError("'interactive' must have a type attribute")

    return payload


def wearable(background_image=None, extra_pages=None, interactive=None):
    """Android wearable payload builder.

    :keyword background_image: Optional string. A URL that specifies the
        background image to display on a wearable device.
    :keyword extra_pages: Optional array of objects.
    :keyword interactive: Optional object. Override the interactive
        notification payload for the wearable device.
    """
    payload = {
        'background_image': background_image,
        'extra_pages': extra_pages,
        'interactive': interactive
    }
    return {key: val for key, val in iter(payload.items()) if val is not None}


def public_notification(title=None, alert=None, summary=None):
    """Android L public notification payload builder.

    :keyword title: Optional string. The notification title.
    :keyword alert: Optional string. The notification alert.
    :keyword summary: Optional string. The notification summary.
    """
    payload = {'title': title, 'alert': alert, 'summary': summary}
    return {key: val for key, val in iter(payload.items()) if val is not None}


def style(style_type, content, title=None, summary=None):
    """Android/Amazon style builder.

    :keyword style_type: String. Must be one of "big_text", "big_picture",
        or "inbox".
    :keyword content: String or array of strings. Content of the style object.
        If style_type is set to "inbox", this will be an array of strings.
        Otherwise, it will be a single string.
    :keyword title: Optional string. Override the notification.
    :keyword summary: Optional string. Override the summary of the
        notification.

    """
    mapping = {
        'big_text': 'big_text', 'big_picture': 'big_picture', 'inbox': 'lines'
    }
    if style_type not in mapping.keys():
        raise ValueError('style_type must be one of {}.'.format(
            ', '.join(mapping.keys())
        ))
    payload = {
        'type': style_type, mapping[style_type]: content,
        'title': title, 'summary': summary
    }
    return {key: val for key, val in iter(payload.items()) if val is not None}


def media_attachment(url, content=None, options=None):
    """iOS media_attachment builder.

    :keyword url: String. Specifies the URL to be downloaded by the UA
        Media Attachment extension.
    :keyword content: Optional dictionary. Describes portions of the
        notification that should be modified if the media attachment
        succeeds. See :func:`content`.
    :keyword options: Optional dictionary. Describes how to display the
        resource given by the URL. See :func:`options`.
    """
    payload = {'url': url, 'content': content, 'options': options}
    return {key: val for key, val in iter(payload.items()) if val is not None}


def content(title=None, subtitle=None, body=None):
    """iOS content builder. Each argument describes the portions of the
    notifcation that should be modified if the media_attachment succeeds.

    :keyword title: String.
    :keyword subtitle: String.
    :keyword body: String.
    """
    payload = {'title': title, 'subtitle': subtitle, 'options': options}
    return {key: val for key, val in iter(payload.items()) if val is not None}


def crop(x=None, y=None, width=None, height=None):
    """iOS crop builder.

    :keyword x: Optional float. The X offset where the crop begins.
    :keyword y: Optional float. The Y offset where the crop begins.
    :keyword width: Optional float. The width of the final crop.
    :keyword height: Optional float. The height of the final crop.
    """
    payload = {'x': x, 'y': y, 'width': width, 'height': height}
    return {key: val for key, val in iter(payload.items()) if val is not None}
