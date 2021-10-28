odoo.define('wagon_basket_route_mapping.MapModelNew', function (require) {
"use strict";

const AbstractModel = require('web.AbstractModel');
const session = require('web.session');
const mapmodel = require('web_map.MapModel');
const core = require('web.core');
const _t = core._t;

mapmodel.include({
__load: function (params) {
console.log("kkkkkkkkkkkkjjjjjjjjjhhhgfddddddd",params)
        console.log("loading...........",params)


        this.data.count = 0;
        this.data.offset = 0;
        this.data.limit = params.limit;
        this.data.filter = [];
        this.partnerToCache = [];
        this.partnerIds = [];
        this.resPartnerField = params.resPartnerField;
        this.model = params.modelName;
        this.data.model = this.model;
        if (this.model == 'sale.order'){
        params.fieldNames = ['partner_id','display_name','route_id','last_assigned','slot'];
        }
        this.context = params.context;
        this.fields = params.fieldNames;
        this.fieldsInfo = params.fieldsInfo;
        this.domain = params.domain;
        this.params = params;
        console.log("this",this.params)
        this.data.result;
        console.log("this",this.data)
        this.data.result = [];
        this.orderBy = params.orderBy;
        this.routing = params.routing;
        this.numberOfLocatedRecords = 0;
        this.coordinateFetchingTimeoutHandle = undefined;
        this.data.shouldUpdatePosition = true;
        this.data.fetchingCoordinates = false;
        this.data.groupBy = params.groupedBy.length ? params.groupedBy[0] : false;
                this.data.domain = this.domain;

        return this._fetchData();
    },


//
//    _fetchData: async function () {
//    console.log("jjjjjjjjjjkkkkkkkkkkk")
//        //case of empty map
//        if (!this.resPartnerField) {
//            this.data.recordGroups = [];
//            this.data.records = [];
//            this.data.routeInfo = { routes: [] };
//            return;
//        }
//        const results = await this._fetchRecordData();
//        console.log("oooooooo",results)
//        console.log("thisparaaaa",this.params)
//        this.data.records = results.records;
//        if (this.model =='sale.order'){
//        var res = this.data.records.reduce(function (r, a) {
//        r[a.route_id[1]] = r[a.route_id[1]] || [];
//        r[a.route_id[1]].push(a);
//        return r;
//    }, Object.create(null));
//    console.log(res);
//
//
//    var lst = [];
//
//    for (var key in res){
//    console.log(key,"key")
//    var dict = {};
//    dict[key] = res[key];
//    var length = res[key].length
//    console.log("length",length);
//    console.log("dict",dict);
//    dict['length'] = length;
//    lst.push(dict)
//    };
//    console.log("kkkk",lst)
//    this.data.result = lst;
//
//        }
//        console.log("6666666",this.data.domain)
//        this.data.count = results.length;
//        console.log("groupp",this.data.groupBy)
//        if (this.data.groupBy) {
//            this.data.recordGroups = this._getRecordGroups();
//        } else {
//            this.data.recordGroups = {};
//        }
//
//        this.partnerIds = [];
//        if (this.model === "res.partner" && this.resPartnerField === "id") {
//            this.data.records.forEach((record) => {
//                this.partnerIds.push(record.id);
//                record.partner_id = [record.id];
//            });
//        } else {
//            this._fillPartnerIds(this.data.records);
//        }
//
//        this.partnerIds = _.uniq(this.partnerIds);
//        console.log('oo',this.data)
//        return this._partnerFetching(this.partnerIds);
//    },

        _getRecordGroups: function () {
    console.log("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    console.log("this.data.groups",this.domain)
    var filters = []
    console.log("filters show yes",filters)
    for (var filter of this.domain){
    filters.push(filter[0])

    }
    if (filters.includes('slot')){
    for (var filter of this.domain){
    if (filter[0] == 'slot'){
    console.log("filter is slot exist")
    this.data.filter[0] = filter[2]
    }

    }

    }
    else{
        this.data.filter = []

    }
        const [fieldName, subGroup] = this.data.groupBy.split(':');
        const dateGroupFormats = {
            year: 'YYYY',
            quarter: '[Q]Q YYYY',
            month: 'MMMM YYYY',
            week: '[W]WW YYYY',
            day: 'DD MMM YYYY',
        };
        const groups = {};
        for (const record of this.data.records) {
            const value = record[fieldName];
            let id, name;
            if (['date', 'datetime'].includes(this.fieldsInfo[fieldName].type)) {
                const date = moment(value);
                id = name = date.format(dateGroupFormats[subGroup]);
            } else {
                id = Array.isArray(value) ? value[0] : value;
                name = Array.isArray(value) ? value[1] : value;
            }
            if (!groups[id]) {
                groups[id] = {
                    name,
                    records: [],
                };
            }
            groups[id].records.push(record);
        }
        return groups;
    },
//        module.exports = {
//  __reload(),
//};

})


}



)