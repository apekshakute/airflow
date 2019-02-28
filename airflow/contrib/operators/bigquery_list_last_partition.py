# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class BigQueryListLastPartitionOperator(BaseOperator):
    """
    :param table_lst: List of tables in format of <project>:<dataset>.<table_name>
    :type table_lst: list of string
    :param bigquery_conn_id: reference to a specific BigQuery hook.
    :type bigquery_conn_id: string
    :param delegate_to: The account to impersonate, if any.
        For this to work, the service account making the request must have domain-wide
        delegation enabled.
    :type delegate_to:
    :return return dictionary of <full_name_name> : <latest_partition_time>
        where latest_partition_time time is in format of YYYYMMDD
    :rtype dict
    """
    template_fields = ('table_lst')
    ui_color = '#e4f0e8'

    @apply_defaults
    def __init__(self,
                 table_lst,
                 bigquery_conn_id='bigquery_default',
                 delegate_to=None,
                 *args,
                 **kwargs):
        super(BigQueryListLastPartitionOperator, self).__init__(*args, **kwargs)
        self.table_lst = table_lst
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        self.log.info('Fetching Data from:')
        self.log.info('Dataset: %s ; Table: %s ; Max Results: %s',
                      self.dataset_id, self.table_id, self.max_results)
        hook = BigQueryHook(bigquery_conn_id=self.bigquery_conn_id,
                            delegate_to=self.delegate_to)
        return_dict = {}
        for each_table in self.table_lst:
            project = each_table.split(':')[0]
            dataset = each_table.split(':')[1].split('.')[0]
            table_name = each_table.split(':')[1].split('.')[1]
            return_dict[each_table] = sorted(hook.table_list_partition(project, dataset, table_name))[-1]
        return return_dict
