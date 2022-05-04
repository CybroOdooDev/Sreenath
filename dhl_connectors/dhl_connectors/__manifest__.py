# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

{
    "name": "DHL Connector",
    "summary": "Compute shipping costs and ship with DHL Parcel Services",
    "images": ["static/description/sendcloud_cover.jpeg"],
    "category": "Operations/Inventory/Delivery",
    "version": "14.0.1.0.0",
    "author": "Onestein",
    "license": "OPL-1",
    "depends": ["delivery", "base_address_extended"],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_view.xml",
        "views/delivery_carrier_view.xml",
        "views/dhl_parcel_view.xml",
        "views/dhl_parcel_status_view.xml",
        "views/dhl_integration_view.xml",
    ],
    "qweb": ["static/src/xml/backend_service_point.xml"],
    "application": True,
}
