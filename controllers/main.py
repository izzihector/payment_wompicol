# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request
from odoo.http import Response

_logger = logging.getLogger(__name__)


class WompiColController(http.Controller):

    @http.route(['/payment/wompicol/response',
                '/payment/wompicol_test/response'],
                type='json', auth='public', csrf=False)
    def wompicol_response(self, **post):
        """ Wompi Colombia """
        # Wompi servers will post the event information
        # {
        #   "event": "transaction.updated",
        #   "data": {
        #     "transaction": {
        #         "id": "01-1532941443-49201",
        #         "amount_in_cents": 4490000,
        #         "reference": "MZQ3X2DE2SMX",
        #         "customer_email": "juan.perez@gmail.com",
        #         "currency": "COP",
        #         "payment_method_type": "NEQUI",
        #         "redirect_url": "https://mitienda.com.co/pagos/redireccion",
        #         "status": "APPROVED",
        #         "shipping_address": null,
        #         "payment_link_id": null,
        #         "payment_source_id": null
        #       }
        #   },
        #   "sent_at":  "2018-07-20T16:45:05.000Z"
        # }
        if post:
            if post.get('data') and post.get('data').get('transaction'):
                _logger.info(
                        'Wompicol: entering form_feedback with\
                                post response data %s', pprint.pformat(post))
                request.env['payment.transaction'].sudo().form_feedback(
                        post, 'wompicol')
            # If has the data return 200
            return Response("Wompi Event Received", status=200)

        # Return to the main page
        return werkzeug.utils.redirect('/')

    @http.route('/payment/wompicol/client_return', type='http',
                auth='public', csrf=False)
    def wompicol_client_return(self, **post):
        """ Wompi Colombia """
        # The client browser will comeback with the following data
        # {
        #   'env': 'test',
        #   'id': '16056-1597266116-33603'
        # }

        if not post:
            post = {}

        _logger.info('Wompicol: client browser returning. %s',
                     pprint.pformat(post))

        return werkzeug.utils.redirect('/payment/process')
