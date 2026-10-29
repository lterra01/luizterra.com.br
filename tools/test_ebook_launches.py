import copy
import unittest

from ebook_catalog import BOOK_TITLES, COLLECTION_COPY, EBOOKS
from ebook_launches import NEW_EBOOKS, RELEASE_CHECKS, released_additions
from voucher_registry import TITLE_IDS


class EBookLaunchTests(unittest.TestCase):
    def test_prepared_additions_have_complete_multilingual_metadata(self):
        self.assertEqual({book['volume'] for book in NEW_EBOOKS}, {4, 5, 6})
        self.assertEqual(len({book['id'] for book in NEW_EBOOKS}), 3)
        for book in NEW_EBOOKS:
            self.assertEqual(set(book['titles']), {'pt', 'en', 'es'})
            self.assertEqual(set(book['summary']), {'pt', 'en', 'es'})
            self.assertEqual(set(book['topics']), {'pt', 'en', 'es'})
            self.assertEqual((book['pages'], book['worksheets'], book['price']), (25, 4, '9.99'))

    def test_drafts_are_not_public_offers_or_voucher_choices(self):
        draft_ids = {book['id'] for book in NEW_EBOOKS if book['release_state'] != 'released'}
        self.assertTrue(draft_ids.isdisjoint(book['id'] for book in EBOOKS))
        self.assertTrue(draft_ids.isdisjoint(BOOK_TITLES))
        self.assertTrue(draft_ids.isdisjoint(TITLE_IDS))
        self.assertEqual(TITLE_IDS, {book['id'] for book in EBOOKS})
        draft = copy.deepcopy(NEW_EBOOKS[0])
        draft['release_state'] = 'draft'
        draft['checks'] = {name: False for name in RELEASE_CHECKS}
        self.assertEqual(released_additions([draft]), [])

    def test_released_additions_have_receipts_and_reach_all_catalogues(self):
        released = released_additions()
        self.assertEqual(len(released), 3)
        self.assertEqual({book['hotmart_id'] for book in released}, {'8836219', '8836306', '8836331'})
        for book in NEW_EBOOKS:
            self.assertTrue(all(book['checks'].values()))
            self.assertIn(book['id'], BOOK_TITLES)
            self.assertIn(book['id'], TITLE_IDS)
        self.assertEqual(len(EBOOKS), 6)

    def test_missing_receipts_block_a_claimed_release(self):
        book = copy.deepcopy(NEW_EBOOKS[0])
        book['release_state'] = 'released'
        for missing in RELEASE_CHECKS:
            book['checks'] = {name: name != missing for name in RELEASE_CHECKS}
            with self.assertRaisesRegex(ValueError, 'Unverified eBook release'):
                released_additions([book])

    def test_release_needs_real_checkout_and_product_id(self):
        book = copy.deepcopy(NEW_EBOOKS[0])
        book['release_state'] = 'released'
        book['checks'] = {name: True for name in RELEASE_CHECKS}
        book['checkout'] = None
        with self.assertRaisesRegex(ValueError, 'Missing verified checkout'):
            released_additions([book])
        book['hotmart_id'] = None
        with self.assertRaisesRegex(ValueError, 'Missing verified Hotmart ID'):
            released_additions([book])

    def test_public_counts_follow_the_released_catalogue(self):
        for copy_text in COLLECTION_COPY.values():
            self.assertIn(f'{len(EBOOKS)} eBooks', copy_text['bar'])


if __name__ == '__main__':
    unittest.main()
