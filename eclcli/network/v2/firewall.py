from eclcli.common import command
from eclcli.common import utils
from ..networkclient.common import utils as to_obj


class ListFirewall(command.Lister):
    def get_parser(self, prog_name):
        parser = super(ListFirewall, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network

        columns = (
            'id',
            'name',
            'status',
        )
        column_headers = (
            'ID',
            'Name',
            'Status',
        )

        data = [to_obj.Firewall(firewall)
                for firewall in network_client.list_firewalls().get('firewalls')]

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                ) for s in data))


class ShowFirewall(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super(ShowFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'firewall_id',
            metavar="FIRWALL_ID",
            help="ID of Firewall to show."
        )
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network

        firewall_id = parsed_args.firewall_id

        dic = network_client.show_firewall(firewall_id).get('firewall')
        columns = utils.get_columns(dic)
        obj = to_obj.Firewall(dic)
        data = utils.get_item_properties(
            obj, columns,)
        return columns, data


class CreateFirewall(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super(CreateFirewall, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='<string>',
            help='Name of firewall to create.')
        parser.add_argument(
            '--description',
            metavar='<string>',
            help='Description of firewall to create.')
        parser.add_argument(
            'firewall_plan_id',
            metavar='FIREWALL_PLAN_ID',
            help='Firewall Plan ID of firewall to create')
        parser.add_argument(
            '--availability_zone',
            metavar='<string>',
            help='Availability Zone of firewall to create.')
        parser.add_argument(
            '--default_gateway',
            metavar='<ipv4>',
            help='Default Gateway of firewall to create.')
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network

        body = {'firewall': {}}
        utils.update_dict(
            parsed_args,
            body['firewall'],
            ['name', 'description', 'firewall_plan_id',
             'availability_zone', 'default_gateway'])

        dic = network_client.create_firewall(body).get('firewall')
        columns = utils.get_columns(dic)
        obj = to_obj.Firewall(dic)
        data = utils.get_item_properties(
            obj, columns,)
        return columns, data


class SetFirewall(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super(SetFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'firewall_id',
            metavar='FIREWALL_ID',
            help='ID of Public IP to update.')
        parser.add_argument(
            '--name',
            metavar='<string>',
            help='Name of firewall to update.')
        parser.add_argument(
            '--description',
            metavar='<string>',
            help='Description of firewall to update.')
        parser.add_argument(
            '--firewall_plan_id',
            metavar='FIREWALL_PLAN_ID',
            help='Firewall Plan ID of firewall to update')
        parser.add_argument(
            '--default_gateway',
            metavar='<ipv4>',
            help='Default Gateway of firewall to update.')
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network

        body = {'firewall': {}}
        firewall_id = parsed_args.firewall_id
        utils.update_dict(
            parsed_args,
            body['firewall'],
            ['name', 'description',
             'firewall_plan_id', 'default_gateway'])

        dic = network_client.update_firewall(
            firewall_id, body).get('firewall')
        columns = utils.get_columns(dic)
        obj = to_obj.Firewall(dic)
        data = utils.get_item_properties(
            obj, columns,)
        return (columns, data)


class DeleteFirewall(command.Command):
    def get_parser(self, prog_name):
        parser = super(DeleteFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'firewall_id',
            metavar="FIRWALL_ID",
            nargs="+",
            help="ID(s) of Firewall to delete."
        )
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network

        for fid in parsed_args.firewall_id:
            network_client.delete_firewall(fid)


class RebootFirewall(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super(RebootFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'firewall_id',
            metavar="FIRWALL_ID",
            help="ID of Firewall to reboot."
        )
        parser.add_argument(
            '--type',
            metavar='{SOFT|HARD}',
            default="HARD",
            choices=["SOFT", "HARD"],
            help='Reboot type: SOFT/HARD.')
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network

        firewall_id = parsed_args.firewall_id

        body = {}
        body.update({"type": parsed_args.type})

        network_client.reboot_firewall(firewall_id, body=body)
        dic = network_client.show_firewall(firewall_id).get("firewall")
        columns = utils.get_columns(dic)
        obj = to_obj.Firewall(dic)
        data = utils.get_item_properties(
            obj, columns,)
        return columns, data


class ResetPasswordFirewall(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super(ResetPasswordFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'firewall_id',
            metavar="FIRWALL_ID",
            help="ID of Firewall to reset password."
        )
        parser.add_argument(
            '--username',
            metavar='USERNAME',
            required=True,
            help='username to reset password of Firewall.')
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network

        firewall_id = parsed_args.firewall_id
        body = {}
        body.update({"username": parsed_args.username})
        dic = network_client.reset_password_firewall(firewall_id, body=body)
        columns = utils.get_columns(dic)
        obj = to_obj.Firewall(dic)
        data = utils.get_item_properties(
            obj, columns,)
        return columns, data
