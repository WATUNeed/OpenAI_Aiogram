import pytest

from Bot import get_button_url


@pytest.mark.parametrize("url, message, result", [
    ('https://cryptoslate.com/binaryx-token-surge-over-9000-following-bnx-split/',
     'Ссылка на источник',
     {"inline_keyboard": [[{"text": "Ссылка на источник", "url": "https://cryptoslate.com/binaryx-token-surge-over-9000-following-bnx-split/"}]]}
     ),
    ('https://cryptoslate.com/coinex-to-stop-serving-all-u-s-customers/',
     'Link',
     {"inline_keyboard": [[{"text": "Link", "url": "https://cryptoslate.com/coinex-to-stop-serving-all-u-s-customers/"}]]}
     ),
    ('https://cryptoslate.com/hashkey-obtains-sfc-approval-to-offer-off-platform-otc-trading/',
     None,
     {"inline_keyboard": [[{"text": "Ссылка на источник", "url": "https://cryptoslate.com/hashkey-obtains-sfc-approval-to-offer-off-platform-otc-trading/"}]]}
     )
])
def test_standard_cases(url, message, result):
    assert get_button_url(url, message), result

