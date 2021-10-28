odoo.define("barcode_action_package.form", function (require) {
    "use strict";
    console.log("0000")


    var FormController = require("web.FormController");

    FormController.include({
        _barcodeHandleAction: function (barcode) {
        console.log(barcode)
            var record = this.model.get(this.handle);
            var self = this;
            return self
                ._rpc({
                    model: record.data.model,
                    method: record.data.method,
                    args: [[record.data.res_id], barcode],
                })
                .then(function (action) {
                    if (action) {
                        self._barcodeStopListening();
                        self.do_action(action);
                    }
                });
        },
    });
});
