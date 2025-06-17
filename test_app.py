import unittest
from unittest.mock import patch, MagicMock
from app import re_rank_cross_encoder, process_document, add_to_collection, query_collection

class TestApp(unittest.TestCase):
    @patch('app.CrossEncoder')
    def test_re_rank_cross_encoder(self, mock_encoder):
        mock_instance = mock_encoder.return_value
        mock_instance.rank.return_value = [
            {"corpus_id": 1}, {"corpus_id": 0}, {"corpus_id": 2}
        ]
        prompt = "What is AI?"
        docs = ["Doc0", "Doc1", "Doc2"]
        relevant_text, relevant_ids = re_rank_cross_encoder(prompt, docs)
        self.assertIn("Doc1", relevant_text)
        self.assertEqual(relevant_ids, [1, 0, 2])

    @patch('app.PyMuPDFLoader')
    @patch('app.tempfile.NamedTemporaryFile')
    def test_process_document(self, mock_tempfile, mock_loader):
        mock_file = MagicMock()
        mock_file.name = 'test.pdf'
        mock_file.read.return_value = b'data'
        mock_temp = MagicMock()
        mock_temp.name = 'tempfile.pdf'
        mock_tempfile.return_value = mock_temp
        # Properly mock a Document with string page_content and dict metadata
        mock_doc = MagicMock()
        mock_doc.page_content = 'This is a test document.'
        mock_doc.metadata = {}
        mock_loader.return_value.load.return_value = [mock_doc]
        with patch('os.unlink'):
            from app import process_document
            result = process_document(mock_file)
            self.assertIsInstance(result, list)
            self.assertTrue(all(hasattr(doc, 'page_content') for doc in result))

    @patch('app.get_vector_collection')
    def test_add_to_collection(self, mock_get_collection):
        mock_collection = MagicMock()
        mock_get_collection.return_value = mock_collection
        splits = [MagicMock(page_content='text', metadata={}) for _ in range(2)]
        add_to_collection(splits, 'file')
        self.assertTrue(mock_collection.upsert.called)

    @patch('app.get_vector_collection')
    def test_query_collection(self, mock_get_collection):
        mock_collection = MagicMock()
        mock_collection.query.return_value = {'documents': [["doc1", "doc2"]]}
        mock_get_collection.return_value = mock_collection
        result = query_collection('prompt')
        self.assertIn('documents', result)

if __name__ == '__main__':
    unittest.main()
