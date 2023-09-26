import unittest
from unittest.mock import patch
# Replace 'your_module' with the actual module name
from base import WordLiftLoader, APICallError

test_key = "X0PARlbAJaLjpuxEoGy4s40MzYi50dqdCv2zoWRdRketAZVEOWvjrX8nxYdgR1nc"


class TestWordLiftLoader(unittest.TestCase):

    @patch('requests.post')
    def test_fetch_data(self, mock_post):
        # Mock the API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'data': {'some_field': 'some_value'},
            'errors': None
        }

        # Initialize the WordLiftLoader object
        loader = WordLiftLoader(
            endpoint='https://api.wordlift.io/graphql/',
            headers={
                "Authorization": f"Key {test_key}",
                "Content-Type": "application/json"
            },
            query="""
                query {
                    entities(query: {
                        descriptionConstraint: {exists: {exists: true, excludeEmpty: true}},
                        wordpressTitleConstraint: {exists: {exists: true, excludeEmpty: true}}
                    }) {
                        headlines: string(name: "wordpress:title")
                        url: string(name: "wordpress:permalink")
                        body: string(name: "wordpress:content")
                    }
                }""",
            fields='entities',
            configure_options={
                "text_fields": ["body"],
                "metadata_fields": ["url", "headlines", "date"],
            }
        )

        # Test the fetch_data method
        self.assertEqual(loader.fetch_data(), {
                         'data': {'some_field': 'some_value'}, 'errors': None})

    @patch('requests.post')
    def test_fetch_data_error(self, mock_post):
        # Mock an API error response
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {
            'data': None,
            'errors': 'Some error'
        }

        # Initialize the WordLiftLoader object
        loader = WordLiftLoader(
            endpoint='https://api.wordlift.io/graphql/',
            headers={
                "Authorization": f"Key {test_key}",
                "Content-Type": "application/json"
            },
            query="""
                query {
                    entities(query: {
                        descriptionConstraint: {exists: {exists: true, excludeEmpty: true}},
                        wordpressTitleConstraint: {exists: {exists: true, excludeEmpty: true}}
                    }) {
                        headlines: string(name: "wordpress:title")
                        url: string(name: "wordpress:permalink")
                        body: string(name: "wordpress:content")
                    }
                }""",
            fields='entities',
            configure_options={
                "text_fields": ["body"],
                "metadata_fields": ["url", "headlines", "date"],
            }
        )

        # Test if APICallError is raised
        with self.assertRaises(APICallError):
            loader.fetch_data()


if __name__ == '__main__':
    unittest.main()
