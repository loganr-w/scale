"""Defines the class that represents resource offers"""
from __future__ import unicode_literals


class ResourceOffer(object):
    """This class represents an offer of resources from a node."""

    def __init__(self, offer_id, agent_id, framework_id, node_resources, when, mesos_offer):
        """Constructor

        :param offer_id: The ID of the offer
        :type offer_id: string
        :param agent_id: The agent ID of the node
        :type agent_id: string
        :param framework_id: The scheduling framework ID
        :type framework_id: string
        :param node_resources: The resources offered by the node
        :type node_resources: :class:`node.resources.node_resources.NodeResources`
        :param when: When the offer was received
        :type when: :class:`datetime.datetime`
        :param mesos_offer: The mesos offer object
        :type mesos_offer: :class:`mesoshttp.offers.Offer`
        """

        self.id = offer_id
        self.agent_id = agent_id
        self.framework_id = framework_id
        self.resources = node_resources
        self.received = when
        self.mesos_offer = mesos_offer
