from jinja2 import Template

import template
from pyswitch.raw.base.interface import Interface as BaseInterface
from pyswitch.utilities import Util


class Interface(BaseInterface):
    """
      The Interface class holds all the actions assocaiated with the Interfaces
      of a NOS device.

      Attributes:
          None
      """

    def __init__(self, callback):
        """
        Interface init function.

        Args:
           callback: Callback function that will be called for each action.

        Returns:
           Interface Object

        Raises:
           None
        """

        super(Interface, self).__init__(callback)

    @property
    def valid_int_types(self):

        return [
            'ethernet',
            'port_channel',
            'loopback',
            've'
        ]

    @property
    def valid_intp_types(self):
        return [
            'ethernet'

        ]

    @property
    def l2_mtu_const(self):
        minimum_mtu = 1548
        maximum_mtu = 9216
        return (minimum_mtu, maximum_mtu)

    @property
    def l3_mtu_const(self):
        minimum_mtu = 1300
        maximum_mtu = 9194
        return (minimum_mtu, maximum_mtu)

    @property
    def l3_ipv6_mtu_const(self):
        minimum_mtu = 1300
        maximum_mtu = 9194
        return (minimum_mtu, maximum_mtu)

    def add_vlan_int(self, vlan_id_list, desc=None):
        """
        Add VLAN Interface. VLAN interfaces are required for VLANs even when
        not wanting to use the interface for any L3 features.

        Args:
            vlan_id: ID for the VLAN interface being created. Value of 2-4096.

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        try:
            data_list = []
            for vlan_id in vlan_id_list:
                if desc:
                    data_list.append(getattr(template, 'vlan_id_desc').format(vlan_id=vlan_id,
                                                                              desc=desc))
                else:
                    data_list.append(getattr(template, 'vlan_id').format(vlan_id=vlan_id))
            str = "".join(data_list)

            config = getattr(template, 'vlan_create').format(vlan_list=str)
            self._callback(config)
            return True

        except Exception as e:
            reason = e.message
            raise ValueError(reason)

    def overlay_gateway(self, **kwargs):
        """

        Creates Overlay Gateway

        Examples:
        >>> import pyswitch.device
        >>> conn = ('10.26.8.210', '22')
        >>> auth = ('admin', 'password')
        >>> with pyswitch.device.Device(conn=conn, auth=auth,connection_type='NETCONF') as dev:
        ...      output = dev.interface.overlay_gateway(gw_name='Leaf1', loopback_id=2,

        ...      gw_type = 'layer2-extension',vni_auto=True,rbridge_id=None)
        ...      output = dev.interface.overlay_gateway(get=True)
        ...      print output
        """
        get_config = kwargs.pop('get', False)

        if not get_config:
            gw_name = kwargs.pop('gw_name')
            gw_type = kwargs.pop('gw_type', 'layer2-extension')
            vni_auto = kwargs.pop('vni_auto', True)
            loopback_id = kwargs.pop('loopback_id', None)
            vni_auto_data = ""
            if vni_auto:
                vni_auto_data = getattr(template, 'overlay_gateway_vni_auto').format()

            config = getattr(template, 'overlay_gateway_create').format(gw_name=gw_name,
                                                                        gw_type=gw_type,
                                                                        loopback_id=loopback_id,
                                                                        vni_auto_data=vni_auto_data)

            self._callback(config)

        if get_config:
            config = getattr(template, 'overlay_gateway_get').format()
            rest_root = self._callback(config, handler='get_config')
            util = Util(rest_root)
            gw_name = util.find(util.root, './/name')
            gw_type = util.find(util.root, './/gw-type')
            loopback_id = util.find(util.root, './/loopback-id')
            activate = True if util.findNode(util.root, './/activate') is not None else False
            vni_auto = True if util.findNode(util.root, './/auto') is not None else False

            return {"gw_name": gw_name,
                    "gw_type": gw_type,
                    'loopback_id': loopback_id,
                    'rbridge_id': 'None',
                    'activate': activate,
                    'vni_auto': vni_auto,
                    }

    def evpn_instance(self, **kwargs):
        """
        >>> import pyswitch.device
        >>> conn = ('10.26.8.210', '22')
        >>> auth = ('admin', 'password')
        >>> with pyswitch.device.Device(conn=conn, auth=auth,connection_type='NETCONF') as dev:
        ...      output = dev.interface.evpn_instance(get=True)
        ...      print output
        ...      output = dev.interface.evpn_instance(evi_name='Leaf1', duplicate_mac_timer=10,

        ...      max_count = '5')
        ...      output = dev.interface.evpn_instance(get=True)
        ...      print output
        """

        get_config = kwargs.pop('get', False)

        if not get_config:
            evi_name = kwargs.pop('evi_name')
            duplicate_mac_timer = kwargs.pop('duplicate_mac_timer')
            max_count = kwargs.pop('max_count')

            t = Template(getattr(template, 'evpn_instance_create'))
            config = t.render(evi_name=evi_name, duplicate_mac_timer=duplicate_mac_timer,
                              duplicate_mac_timer_max_count=max_count)
            self._callback(config)

        if get_config:
            config = getattr(template, 'evpn_instance_get').format()
            rest_root = self._callback(config, handler='get_config')
            util = Util(rest_root)
            evi_name = util.find(util.root, './/instance-name')
            duplicate_mac_timer = util.find(util.root, './/duplicate-mac-timer-value')
            max_count = util.find(util.root, './/max-count')

            return {"evi_name": evi_name,
                    "duplicate_mac_timer": duplicate_mac_timer,
                    'max_count': max_count
                    }
