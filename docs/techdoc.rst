vk-search documentation
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: vksearch.bot.__main__
    :members:
    :private-members:

.. automodule:: vksearch.bot.vk_requests          
    :members:
    :private-members:

    .. autofunction:: vksearch.bot.vk_requests.get_members_script(api, group_id, offset, count, per_req)

        Vkscript to get group members with offset.

        :param api: vk api
        :type api: vkbottle.API

        :param group_id: group id
        :type group_id: int

        :param offset: offset to start from
        :type offset: int

        :param count: count of users to get
        :type count: int

        :param per_req: count of users to get per single api call
        :type per_req: int

        :return: dict

    .. autofunction:: vksearch.bot.vk_requests.get_friends_script(api, group_id, offset, count, per_req)

        Vkscript to get user friends with offset.

        :param api: vk api
        :type api: vkbottle.API

        :param user_id: user id
        :type user_id: int

        :param offset: offset to start from
        :type offset: int

        :param count: count of users to get
        :type count: int

        :param per_req: count of users to get per single api call
        :type per_req: int

        :return: dict

.. automodule:: vksearch.bot.vk_filters        
    :members:
    :private-members:

.. automodule:: vksearch.bot.limited_client          
    :members:
    :private-members:

