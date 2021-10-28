odoo.define('web_map.MapRenderer', function(require) {
	"use strict";
	var AbstractAction = require('web.AbstractAction');
	var core = require('web.core');
	var field_utils = require('web.field_utils');
	var rpc = require('web.rpc');
	var session = require('web.session');
	var utils = require('web.utils');
	var QWeb = core.qweb;
	var ajax = require('web.ajax');
	var web_map_mod = require('web_map.MapModel');
	var _t = core._t;

	const AbstractRendererOwl = require('web.AbstractRendererOwl');



	const {
		useRef,
		useState
	} = owl.hooks;

	const apiTilesRouteWithToken =
		'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}';
	const apiTilesRouteWithoutToken = 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png';

	const colors = [
		'#F06050',
		'#6CC1ED',
		'#F7CD1F',
		'#814968',
		'#30C381',
		'#D6145F',
		'#475577',
		'#F4A460',
		'#EB7E7F',
		'#2C8397',
	];

	const mapTileAttribution = `
        © <a href="https://www.mapbox.com/about/maps/">Mapbox</a>
        © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>
        <strong>
            <a href="https://www.mapbox.com/map-feedback/" target="_blank">
                Improve this map
            </a>
        </strong>`;

	class MapRenderer extends AbstractRendererOwl {
		/**
		 * @constructor
		 */

		constructor() {
			super(...arguments);
			this.leafletMap = null;
			this.markers = [];
			this.polylines = [];
			this.mapContainerRef = useRef('mapContainer');
			this.state = useState({
				closedGroupIds: [],
			});
		}
		/**
		 * Load marker icons.
		 *
		 * @override
		 */
		async willStart() {
			const p = {
				method: 'GET'
			};
			[this._pinCircleSVG, this._pinNoCircleSVG] = await Promise.all([
				this.env.services.httpRequest('web_map/static/img/pin-circle.svg', p, 'text'),
				this.env.services.httpRequest('web_map/static/img/pin-no-circle.svg', p, 'text'),
			]);
			return super.willStart(...arguments);
		}
		/**
		 * Initialize and mount map.
		 *
		 * @override
		 */
		mounted() {
			this.leafletMap = L.map(this.mapContainerRef.el, {
				maxBounds: [L.latLng(180, -180), L.latLng(-180, 180)],
			});
			L.tileLayer(this.apiTilesRoute, {
				attribution: mapTileAttribution,
				tileSize: 512,
				zoomOffset: -1,
				minZoom: 2,
				maxZoom: 19,
				id: 'mapbox/streets-v11',
				accessToken: this.props.mapBoxToken,
			}).addTo(this.leafletMap);
			this._updateMap();
			super.mounted(...arguments);
		}
		/**
		 * Update position in the map, markers and routes.
		 *
		 * @override
		 */
		patched() {
			this._updateMap();
			super.patched(...arguments);
		}
		/**
		 * Update group opened/closed state.
		 *
		 * @override
		 */
		willUpdateProps(nextProps) {
			if (this.props.groupBy !== nextProps.groupBy) {
				this.state.closedGroupIds = [];
			}
			return super.willUpdateProps(...arguments);
		}
		/**
		 * Remove map and the listeners on its markers and routes.
		 *
		 * @override
		 */
		willUnmount() {
			for (const marker of this.markers) {
				marker.off('click');
			}
			for (const polyline of this.polylines) {
				polyline.off('click');
			}
			this.leafletMap.remove();
			super.willUnmount(...arguments);
		}

		//----------------------------------------------------------------------
		// Getters
		//----------------------------------------------------------------------

		/**
		 * Return the route to the tiles api with or without access token.
		 *
		 * @returns {string}
		 */
		get apiTilesRoute() {
			return this.props.mapBoxToken ? apiTilesRouteWithToken : apiTilesRouteWithoutToken;
		}

		//----------------------------------------------------------------------
		// Private
		//----------------------------------------------------------------------

		/**
		 * If there's located records, adds the corresponding marker on the map.
		 * Binds events to the created markers.
		 *
		 * @private
		 */
		_addMarkers() {
			console.log("addmarkers")
			this._removeMarkers();
			console.log("markersssssss", this.markers)

			const markersInfo = {};
			let records = this.props.records;
			console.log("888888888", records)
			if (this.props.groupBy) {
				records = Object.entries(this.props.recordGroups)
					.filter(([key]) => !this.state.closedGroupIds.includes(key))
					.flatMap(([, value]) => value.records);
			}

			for (const record of records) {
				const partner = record.partner;
				if (partner && partner.partner_latitude && partner.partner_longitude) {
					const key = `${partner.partner_latitude}-${partner.partner_longitude}`;
					if (key in markersInfo) {
						markersInfo[key].record = record;
						markersInfo[key].ids.push(record.id);
					} else {
						markersInfo[key] = {
							record: record,
							ids: [record.id]
						};
					}
				}
			}

			for (const markerInfo of Object.values(markersInfo)) {
				const params = {
					count: markerInfo.ids.length,
					isMulti: markerInfo.ids.length > 1,
					number: this.props.records.indexOf(markerInfo.record) + 1,
					numbering: this.props.numbering,
					pinSVG: (this.props.numbering ? this._pinNoCircleSVG : this._pinCircleSVG),
				};

				if (this.props.groupBy) {
					const group = Object.entries(this.props.recordGroups)
						.find(([, value]) => value.records.includes(markerInfo.record));
					params.color = this._getGroupColor(group[0]);
				}

				// Icon creation
				const iconInfo = {
					className: 'o_map_marker',
					html: this.env.qweb.renderToString('web_map.marker', params),
				};

				// Attach marker with icon and popup
				const marker = L.marker([
					markerInfo.record.partner.partner_latitude,
					markerInfo.record.partner.partner_longitude
				], {
					icon: L.divIcon(iconInfo)
				});
				marker.addTo(this.leafletMap);
				marker.on('click', () => {
					this._createMarkerPopup(markerInfo);
				});
				console.log("marker new", marker)
				this.markers.push(marker);
			}
			if (this.props.filter[0]) {
				console.log("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
			}
		}
		/**
		 * If there are computed routes, create polylines and add them to the map.
		 * each element of this.props.routeInfo[0].legs array represent the route between
		 * two waypoints thus each of these must be a polyline.
		 *
		 * @private
		 */
		_addRoutes() {
			this._removeRoutes();
			if (!this.props.mapBoxToken || !this.props.routeInfo.routes.length) {
				return;
			}

			for (const leg of this.props.routeInfo.routes[0].legs) {
				const latLngs = [];
				for (const step of leg.steps) {
					for (const coordinate of step.geometry.coordinates) {
						latLngs.push(L.latLng(coordinate[1], coordinate[0]));
					}
				}

				const polyline = L.polyline(latLngs, {
					color: 'blue',
					weight: 5,
					opacity: 0.3,
				}).addTo(this.leafletMap);

				const polylines = this.polylines;
				polyline.on('click', function() {
					for (const polyline of polylines) {
						polyline.setStyle({
							color: 'blue',
							opacity: 0.3
						});
					}
					this.setStyle({
						color: 'darkblue',
						opacity: 1.0
					});
				});
				this.polylines.push(polyline);
			}
		}
		/**
		 * Create a popup for the specified marker.
		 *
		 * @private
		 * @param {Object} markerInfo
		 */
		_createMarkerPopup(markerInfo) {
			var self = this;
			//                        this.props.groupBy = 'partner_id'
			//console.log("self 2.0.......................",this.props)

			rpc.query({
				model: 'sale.order',
				method: 'find_route',
				args: [0],
			}).then(function(domains) {
				console.log("Success", domains)
				var domain_route = domains
				const popupFields = self._getMarkerPopupFields(markerInfo);
				const route_records = self.props.result;
				const partner = markerInfo.record.partner;
				//            var journal_ids = [];
				//            var journal_text = [];
				//            var span_res = document.getElementById("route_res")
				//            var journal_list = $(".route").select2('data')
				//            console.log("Lllllllllll",journal_list)
				//            for (var i = 0; i < journal_list.length; i++) {
				//            if(journal_list[i].element[0].selected === true){ journal_ids.push(parseInt(journal_list[i].id))
				//            if(journal_text.includes(journal_list[i].text) === false){
				//            journal_text.push(journal_list[i].text)
				//            }
				//            span_res.value = journal_text
				//            span_res.innerHTML=span_res.value;
				//            }
				//            }
				//            if (journal_list.length == 0){
				//            span_res.value = ""
				//            span_res.innerHTML=""; }
				//            output.journal_ids = journal_ids
				//var vals = this.props.result;


				console.log("jjjjjjjjjjj", domain_route)
								console.log("modellll",self.props.model)


                if (self.props.model == 'sale.order'){
                var records = markerInfo.record.route_id[1]
                }else{
                var records = ''
                }
				const popupHtml = self.env.qweb.renderToString('web_map.markerPopup', {
					fields: popupFields,
					records: records,
					routes: domain_route,
					hasFormView: self.props.hasFormView,
					url: `https://www.google.com/maps/dir/?api=1&destination=${partner.partner_latitude},${partner.partner_longitude}`,
				});

				const popup = L.popup({
						offset: [0, -30]
					})
					.setLatLng([partner.partner_latitude, partner.partner_longitude])
					.setContent(popupHtml)
					.openOn(self.leafletMap);

				const openBtn = popup.getElement().querySelector('button.o_open');
				if (openBtn) {
					openBtn.onclick = () => {
						self.trigger('open_clicked', {
							ids: markerInfo.ids
						});
					};
				}
				const route_btn = popup.getElement().querySelector('select.route_fetch');
				if (route_btn) {
					route_btn.onclick = () => {
						console.log("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", route_btn.value)
						var route_new = popup.getElement().querySelector('span.routes_res')
						route_new.innerHTML = route_btn.options[route_btn.selectedIndex].text
						var r_val = {
							'r_id': route_btn.value,
							'order_id': markerInfo.record.id
						}
						console.log("h", r_val)
						return rpc.query({
							model: 'sale.order',
							method: 'get_route',
							args: [r_val],
						}).then(function(result) {
							console.log("kkkkkkkkkki")
							var html_content = $('.o_cp_searchview').html();
							console.log("html_content", html_content);
							for (var route of domain_route) {
								console.log("kjhgfr", route)
								if (route[1] == r_val['r_id']) {
									markerInfo.record.route_id[1] = route[0]

								}
							}
							//                markerInfo.record.route_id[0] = r_val['r_id']
							//                markerInfo.record.route_id[1] = r_val['order_id']

							//                location.reload()
							//_reload: function(message, controller) {
							//		if(controller && controller.widget) {
							//		}
							//    },
							//    $( ".o_map_container" ).load(window.location.href + " .o_map_container" );

							//                console.log("*****************",web_map_mod);
							//                self._updateMap();
							//                self._getGroupColor(r_val['r_id'])
							//    const { __reload } = require ('web_map.MapModel');
							//
							//__reload();
							//web_map_mod.prototype.__get();
							//var fil = ['slot','=']
							//fil.push(self.props.filter[0])
							//self.props.domain.push(fil)
							//self.props.domain[0] = '&'
							//web_map_mod.prototype.__reload(params);
							//
							//               document.getElementByClass(".o_map_view").innerHTML.reload;
							//location.reload()
							//                console.log("hhhh..>>",self.props)
							//self.__reload()
							//location.reload()
							//                self.reload();
							//                return false;
							//location.reload();
							//$('.active').removeClass('active'); // removes the active class from other link
							//     $(this).addClass('active'); // adds the active class to current cliked link
							//     setInterval(function(){
							//       $(".o_map_view").load($('.active'),{},function(){}); // populates the div with data-url of active class.
							//     }, 5000);
							//});

							console.log("self.......................", self.props)


							//        $('.o_map_view').load('ajax.html.o_map_view');
							//                    location.reload();
							//        web_map_mod.prototype.__reload(self);

							//location.load(window.location.href + ' .o_content');

							//                $('.o_cp_searchview').html(html_content);
							//$(".o_map_view").load(window.location.href + ".o_map_view");
							//return false;
						})

					};
				}
			})



		}
		/**
		 * @private
		 * @param {Number} groupId
		 */
		_getGroupColor(groupId) {
			console.log("ivvv", groupId)
			const index = Object.keys(this.props.recordGroups).indexOf(groupId);
			return colors[index % colors.length];
		}
		/**
		 * Creates an array of latLng objects if there is located records.
		 *
		 * @private
		 * @returns {latLngBounds|boolean} objects containing the coordinates that
		 *          allows all the records to be shown on the map or returns false
		 *          if the records does not contain any located record.
		 */
		_getLatLng() {
			const tabLatLng = [];
			for (const record of this.props.records) {
				const partner = record.partner;
				if (partner && partner.partner_latitude && partner.partner_longitude) {
					tabLatLng.push(L.latLng(partner.partner_latitude, partner.partner_longitude));
				}
			}
			if (!tabLatLng.length) {
				return false;
			}
			return L.latLngBounds(tabLatLng);
		}

		/**
		 * Get the fields' name and value to display in the popup.
		 *
		 * @private
		 * @param {Object} markerInfo
		 * @returns {Object} value contains the value of the field and string
		 *                   contains the value of the xml's string attribute
		 */
		_getMarkerPopupFields(markerInfo) {
			console.log("markerinfo", markerInfo)
			console.log("markerinfoprop", this.props)
			if (this.props.model == 'stock.picking') {
				this.props.hideAddress = false;
			}

			const record = markerInfo.record;
			const fieldsView = [];
			// Only display address in multi coordinates marker popup
			if (markerInfo.ids.length > 1) {
				if (!this.props.hideAddress) {
					fieldsView.push({
						value: record.partner.contact_address_complete,
						string: this.env._t("Address"),
					});
				}
				return fieldsView;
			}
			if (!this.props.hideName) {
				fieldsView.push({
					value: record.display_name,
					string: this.env._t("Name"),
				});
			}
			if (!this.props.hideAddress) {
				console.log("heyyy")
				fieldsView.push({
					value: record.partner.contact_address_complete,
					string: this.env._t("Address"),
				});
			}
			if (this.props.model != 'stock.picking') {
				for (const field of this.props.fieldNamesMarkerPopup) {
					if (record[field.fieldName]) {
						const fieldName = record[field.fieldName] instanceof Array ?
							record[field.fieldName][1] :
							record[field.fieldName];
						fieldsView.push({
							value: fieldName,
							string: field.string,
						});
					}
				}
			}


			console.log("fieldsview", fieldsView)
			var model = this.props.model
			console.log(";;;;", fieldsView, model)
			var dict = {
				'value': model,
				'string': 'model'
			}
			fieldsView.push(dict)
			return fieldsView;
		}
		/**
		 * Remove the markers from the map and empty the markers array.
		 *
		 * @private
		 */
		_removeMarkers() {
			for (const marker of this.markers) {
				this.leafletMap.removeLayer(marker);
			}
			this.markers = [];
		}
		/**
		 * Remove the routes from the map and empty the the polyline array.
		 *
		 * @private
		 */
		_removeRoutes() {
			for (const polyline of this.polylines) {
				this.leafletMap.removeLayer(polyline);
			}
			this.polylines = [];
		}
		/**
		 * Update position in the map, markers and routes.
		 *
		 * @private
		 */

		_updateMap() {
			console.log("update")
			if (this.props.shouldUpdatePosition) {
				console.log("hirr")
				const initialCoord = this._getLatLng();
				if (initialCoord) {
					this.leafletMap.flyToBounds(initialCoord, {
						animate: false
					});
				} else {
					this.leafletMap.fitWorld();
				}
				this.leafletMap.closePopup();
			}
			this._addMarkers();
			this._addRoutes();
		}

		//----------------------------------------------------------------------
		// Handlers
		//----------------------------------------------------------------------

		/**
		 * Center the map on a certain pin and open the popup linked to it.
		 *
		 * @private
		 * @param {Object} record
		 */
		_centerAndOpenPin(record) {
			this._createMarkerPopup({
				record: record,
				ids: [record.id],
			});
			this.leafletMap.panTo([
				record.partner.partner_latitude,
				record.partner.partner_longitude,
			], {
				animate: true,
			});
		}
		/**
		 * @private
		 * @param {Number} id
		 */
		_toggleGroup(id) {
			if (this.state.closedGroupIds.includes(id)) {
				const index = this.state.closedGroupIds.indexOf(id);
				this.state.closedGroupIds.splice(index, 1);
			} else {
				this.state.closedGroupIds.push(id);
			}
		}
	}
	MapRenderer.props = {
		arch: Object,
		count: Number,
		model: String,
		defaultOrder: {
			type: String,
			optional: true,
		},
		fetchingCoordinates: Boolean,
		fieldNamesMarkerPopup: {
			type: Array,
			element: {
				type: Object,
				shape: {
					fieldName: String,
					string: String,
				},
			},
		},
		groupBy: [String, Boolean],
		hasFormView: Boolean,
		hideAddress: Boolean,
		hideName: Boolean,
		isEmbedded: Boolean,
		limit: Number,
		mapBoxToken: {
			type: [Boolean, String],
			optional: 1
		},
		noContentHelp: {
			type: String,
			optional: true,
		},
		numbering: Boolean,
		hideTitle: Boolean,
		panelTitle: String,
		offset: Number,
		partners: {
			type: [Array, Boolean],
			optional: 1
		},
		recordGroups: Object,
		records: Array,
		filter: Array,
		routeInfo: {
			type: Object,
			optional: true,
		},
		routing: Boolean,
		result: Array,
		routingError: {
			type: String,
			optional: true,
		},
		shouldUpdatePosition: Boolean,
		domain: Array,
	};
	MapRenderer.template = 'web_map.MapRenderer';

	return MapRenderer;
});