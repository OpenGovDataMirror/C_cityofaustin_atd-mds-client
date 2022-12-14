#!/usr/bin/env python

# Required Libraries
import json
from parent_directory import *
from mds.MDSClient import MDSClient
import pdb

class TestMDS030:
    config = None
    client = None

    def setup_class(self):
        print("\n\n---------------------------------------------")
        print("Beginning tests for: TestMDS030")
        print("---------------------------------------------")
        with open("tests/config.json", "r") as json_file:
            self.config = json.load(json_file)

        if isinstance(self.config, dict) is False:
            raise Exception("Configuration file 'tests/config.json' could not be loaded.")

        self.client = MDSClient(config=self.config["jump"])

    def teardown_class(self):
        print("\n\n---------------------------------------------")
        print("All tests finished for: TestMDS030")
        print("---------------------------------------------")
        self.config = None
        self.client = None

    def test_constructor_success_t1(self):
        """
        Tests if the client initialized correctly.
        """
        assert isinstance(self.client, MDSClient)

    def test_constructor_fail_t1(self):
        """
        Tests if the client fails at the lack of a configuration.
        """
        try:
            MDSClient(config=None)
            assert False
        except:
            assert True

    def test_schema_success_t1(self):
        """
        Tests if the load_params value provides the correct schema
        """
        self.client.mds_client._load_params(
            start_time=1578780000,
            end_time=1578783600
        )
        valid_schema = (
                "min_end_time" in self.client.mds_client.params and
                "max_end_time" in self.client.mds_client.params
        )
        assert valid_schema

    def test_params_success_t1(self):
        """
        Tests if the parameters are valid
        """
        valid_params = (
                "min_end_time" in self.client.mds_client.params and
                "max_end_time" in self.client.mds_client.params and
                self.client.mds_client.params["min_end_time"] == 1578780000000 and
                self.client.mds_client.params["max_end_time"] == 1578783600000
        )
        assert valid_params

    def test_get_trips_success_t1(self):
        """
        Tests if the trips response includes version 0.3.0
        """
        trips = self.client.get_trips(
            start_time=1578780000,
            end_time=1578783600
        )
        trips_version = trips.get("version")
        assert isinstance(trips, dict) and \
            trips_version is not None and \
            (trips_version[0:3] == "0.3")
