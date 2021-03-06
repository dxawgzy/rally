# Copyright 2015: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from rally import exceptions
from rally.plugins.openstack.scenarios.ironic import nodes
from tests.unit import test


class IronicNodesTestCase(test.ScenarioTestCase):

    def test_create_and_list_node(self):
        scenario = nodes.CreateAndListNode(self.context)
        scenario._create_node = mock.Mock(return_value="node_obj1")
        scenario._list_nodes = mock.Mock(return_value=["node_obj1",
                                                       "node_obj2",
                                                       "node_obj3"])
        fake_params = {
            "sort_dir": "foo1",
            "associated": "foo2",
            "sort_key": "foo3",
            "detail": True,
            "limit": "foo4",
            "maintenance": "foo5",
            "marker": "foo6",
            "fake_parameter1": "foo7"
        }

        # Positive case:
        scenario.run(**fake_params)

        scenario._create_node.assert_called_once_with(fake_parameter1="foo7")
        scenario._list_nodes.assert_called_once_with(
            sort_dir="foo1", associated="foo2", sort_key="foo3", detail=True,
            limit="foo4", maintenance="foo5", marker="foo6")

        # Negative case1: node isn't created
        scenario._create_node = mock.Mock(return_value=None)
        self.assertRaises(exceptions.RallyAssertionError,
                          scenario.run,
                          **fake_params)

        scenario._create_node.assert_called_with(fake_parameter1="foo7")

        # Negative case2: cretaed node not in the list of available nodes
        scenario._create_node = mock.Mock()
        self.assertRaises(exceptions.RallyAssertionError,
                          scenario.run,
                          **fake_params)

        scenario._create_node.assert_called_with(fake_parameter1="foo7")
        scenario._list_nodes.assert_called_with(
            sort_dir="foo1", associated="foo2", sort_key="foo3", detail=True,
            limit="foo4", maintenance="foo5", marker="foo6")

    def test_create_and_delete_node(self):
        fake_node = mock.Mock(uuid="fake_uuid")
        scenario = nodes.CreateAndDeleteNode(self.context)
        scenario._create_node = mock.Mock(return_value=fake_node)
        scenario._delete_node = mock.Mock()

        scenario.run(fake_parameter1="fake1", fake_parameter2="fake2")
        scenario._create_node.assert_called_once_with(fake_parameter1="fake1",
                                                      fake_parameter2="fake2")

        scenario._delete_node.assert_called_once_with("fake_uuid")
