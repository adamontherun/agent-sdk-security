"""Chapter 3 challenge — review a deployment against least privilege.

The secure-deployment guide gives a least-privilege table: for each resource
an agent touches, restrict it to only what the task needs.

  Filesystem           mount only needed directories, prefer read-only
  Network              restrict to specific endpoints via a proxy
  Credentials          inject via a proxy rather than exposing directly
  System capabilities  drop Linux capabilities in containers

Implement `review_least_privilege` to flag which of these four resources a
deployment leaves under-restricted.
"""


def review_least_privilege(config: dict) -> list[str]:
    """Return the sorted list of resources that violate least privilege.

    `config` may contain these boolean keys (any missing key is treated as
    False):

      "filesystem_writable_root"   root filesystem is writable, not read-only
      "network_unrestricted"       agent can reach any endpoint, no proxy
      "credentials_in_agent_env"   credentials live in the agent's environment
      "linux_caps_dropped"         Linux capabilities have been dropped

    A resource is a violation when it is under-restricted:

      "filesystem"           when filesystem_writable_root is True
      "network"              when network_unrestricted is True
      "credentials"          when credentials_in_agent_env is True
      "system_capabilities"  when linux_caps_dropped is False

    Return the violating resource names sorted alphabetically.
    """
    raise NotImplementedError()
