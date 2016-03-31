from test.test_runner import BaseAsyncTest
import tornado.testing
import time
import rethinkdb as r
import logging

class TestModelData(BaseAsyncTest):

    def setUpClass():
        logging.disable(logging.CRITICAL)

    def test_fcq_model_data(self):
        fcq_model = self.application.settings['fcq']
        cursor = fcq_model.cursor()
        for doc in cursor:
            verified = fcq_model.verify(doc)
            self.assertEqual(len(verified), 0, "FCQ failed verification:\n{0}\n{1}".format(doc['id'], verified))
        cursor.close()

    def tearDownClass():
        logging.disable(logging.NOTSET)
