# coding=utf-8
"""Tests that container repositories have RBAC."""
import unittest

from pulp_smash import cli, config, exceptions, utils
from pulp_smash.pulp3.bindings import monitor_task

from pulp_container.tests.functional.utils import (
    del_user,
    gen_user,
    skip_if,
)

from pulp_container.tests.functional.utils import gen_container_client

from pulpcore.client.pulp_container.exceptions import ApiException
from pulpcore.client.pulp_container import RepositoriesContainerPushApi


cfg = config.get_config()

api_client = gen_container_client()
push_repositories_api = RepositoriesContainerPushApi(api_client)
registry = cli.RegistryClient(cfg)

class RegistryRBACTestCase(unittest.TestCase):
    """
    Tests for the Registry API RBAC.
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables and prepare api users."""
        cls.user1 = gen_user(["container.add_containerdistribution", "container.view_containerdistribution", "container.add_containernamespace"])
        cls.user2 = gen_user(["container.add_containerdistribution", "container.view_containerdistribution", "container.add_containernamespace"])
        cls.repository = None

    @classmethod
    def tearDownClass(cls):
        """Delete api users."""
        del_user(cls.user1)
        del_user(cls.user2)

    def test_01_push_new_repository(self):
        registry.raise_if_unsupported(unittest.SkipTest, "Test requires podman/docker")
        # TODO better handling of the "http://"
        registry_name = cfg.get_base_url()[7:]
        local_url = "/".join([registry_name, "{}/bar:1.0".format(self.user1["username"])])
        # Be sure to not being logged in
        try:
            registry.logout(registry_name)
        except exceptions.CalledProcessError:
            pass
        # Pull an image with large blobs
        registry.pull("busybox:latest")
        # Tag it to registry under test
        registry.tag("busybox:latest", local_url)
        # Try to push without logging in
        with self.assertRaises(exceptions.CalledProcessError):
            registry.push(local_url)
        # Log in
        registry.login("-u", self.user1["username"], "-p", self.user1["password"], registry_name)
        # Push successfully
        registry.push(local_url)
        # Pull while logged in as user1
        registry.pull(local_url)
        # Log out
        registry.logout(registry_name)
        # Login as user2 and assert that user can't push or pull
        registry.login("-u", self.user2["username"], "-p", self.user2["password"], registry_name)
        # Create a new tag and assert that User 2 can't push it to User 1's repository
        local_url2 = "/".join([registry_name, "{}/bar:2.0".format(self.user1["username"])])
        registry.tag("busybox:latest", local_url2)
        with self.assertRaises(exceptions.CalledProcessError):
            registry.push(local_url2)
        # Assert that User 2 is allowed to pull from User 1's repository
        registry.pull(local_url)
        # Untag local copie
        registry.rmi(local_url)
        registry.rmi(local_url2)
        # cleanup
