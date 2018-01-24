import pandas as pd
from flask_testing import TestCase

from cellphonedb.api import create_app, output_dir
from cellphonedb.extensions import db
from cellphonedb.models.gene.db_model_gene import Gene


class DatabaseIntegrity(TestCase):
    def test_gene(self):
        query = db.session.query(Gene)
        dataframe = pd.read_sql(query.statement, db.engine)

        duplicated_genes = dataframe[dataframe.duplicated(keep=False)]
        if len(duplicated_genes):
            duplicated_genes.sort_values('gene_name').to_csv('%s/WARNING_duplicated_genes.csv' % output_dir,
                                                             index=False)

        self.assertEqual(len(duplicated_genes), 0,
                         'There are %s duplicated genes in database. Please check WARNING_duplicated_genes.csv file' % len(
                             duplicated_genes))

    def create_app(self):
        return create_app(environment='test')

    def setUp(self):
        self.client = self.app.test_client()
