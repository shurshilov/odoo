/* @odoo-module */
import {registry} from "@web/core/registry";
import FieldGeoEngineEditMap from "base_geoengine.geoengine_widgets";
import GeoengineView  from 'base_geoengine.GeoengineView';
import BackgroundLayers from 'base_geoengine.BackgroundLayers';
import view_registry from 'web.view_registry';
const {xml, Component, onMounted, onWillStart} = owl;
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { loadBundle, loadJS } from "@web/core/assets";
// Add the field to the correct category

const inherits = function (subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
    constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
    }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
};

export class FieldGeoEngineEditMapOwl extends Component {
    setup() {
        super.setup();
        this.geoType = null;
        this.map= null;
        this.defaultExtent= null;
        this.format= null;
        this.vectorLayer= null;
        this.rasterLayers= null;
        this.source= null;
        this.features= null;
        this.drawControl= null;
        this.modifyControl= null;
        this.tabListenerInstalled= false;

        onWillStart(async () => {
            await loadBundle({
                cssLibs: [
                    // '/base_geoengine/static/lib/ol-4.6.5/ol.css',
                    // '/base_geoengine/static/lib/ol-6.5.0/ol.css',
                    '/base_geoengine/static/lib/ol-5.3.3/ol.css',
                    '/base_geoengine/static/lib/ol3-layerswitcher.css',
                    // '/base_geoengine/static/lib/geostats-1.4.0/geostats.css',
                    '/base_geoengine/static/lib/geostats-2.0.0/geostats.css',
                ],
                jsLibs: [
                    '/mass_mailing/static/src/js/mass_mailing_link_dialog_fix.js',
                    '/base_geoengine/static/lib/ol-5.3.3/ol.js',
                    '/base_geoengine/static/lib/ol3-layerswitcher.js',
                    '/base_geoengine/static/lib/chromajs-0.8.0/chroma.js',
                    '/base_geoengine/static/lib/geostats-2.0.0/geostats.js',
                ],
            });
        });

        onMounted(this.mounted);
    }

    // --------------------------------------------------------------------
    // Public
    // --------------------------------------------------------------------

    mounted() {
        this.bgLayers= new BackgroundLayers();
        this._addTabListener();
        this._render();
    }

    // FIXME still used?
    validate () {
        this.invalid = false;
    }

    // --------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------

    _createVectorLayer () {
        this.features = new ol.Collection();
        this.source = new ol.source.Vector({features: this.features});
        return new ol.layer.Vector({
            source: this.source,
            style: new ol.style.Style({
                fill: new ol.style.Fill({
                    color: '#ee9900',
                    opacity: 0.7,
                }),
                stroke: new ol.style.Stroke({
                    color: '#ee9900',
                    width: 3,
                    opacity: 1,
                }),
                image: new ol.style.Circle({
                    radius: 7,
                    fill: new ol.style.Fill({
                        color: '#ffcc33',
                    }),
                }),
            }),
        });
    }

    _createLayers (field_infos) {
        this.vectorLayer = this._createVectorLayer();
        this.rasterLayers = this.bgLayers.create([
            field_infos.edit_raster,
        ]);
        if (this.rasterLayers.length) {
            this.rasterLayers[0].isBaseLayer = true;
        }
    }

    _addTabListener () {
        if (this.tabListenerInstalled) {
            return;
        }
        var tab = $(this.__owl__.bdom.el).closest('div.tab-pane');
        if (!tab.length) {
            return;
        }
        var tab_link = $('a[href="#' + tab[0].id + '"]')
        if (!tab_link.length) {
            return;
        }
        tab_link.on('shown.bs.tab', function (e) {
            this._render();
        }.bind(this));
        this.tabListenerInstalled = true;
    }

    _parseValue (value) {
        return value;
    }

    _updateMapEmpty () {
        var map_view = this.map.getView();
        // Default extent
        if (map_view) {
            var extent = this.defaultExtent.replace(/\s/g, '').split(',');
            extent = extent.map(coord => Number(coord));
            map_view.fit(extent, {maxZoom: this.defaultZoom || 5});
        }
    }

    _updateMapZoom (zoom) {

        var map_zoom = typeof zoom === 'undefined' ? true : zoom;

        if (this.source) {
            var extent = this.source.getExtent();
            var infinite_extent = [
                Infinity, Infinity, -Infinity, -Infinity,
            ];
            if (map_zoom && extent !== infinite_extent) {
                var map_view = this.map.getView();
                if (map_view) {
                    map_view.fit(extent, {maxZoom: 15});
                }
            }
        }
    }

    _setValue (value, zoom) {

        // this._super(value);
        this.value = value;

        if (this.map) {

            var ft = new ol.Feature({
                geometry: new ol.format.GeoJSON().readGeometry(value),
                labelPoint:  new ol.format.GeoJSON().readGeometry(value),
            });
            this.source.clear();
            this.source.addFeature(ft);
            if (value) {
                this._updateMapZoom(zoom);
            } else {
                this._updateMapEmpty();
            }
        }
    }

    _isTabVisible () {
        var tab = $(this.__owl__.bdom.el).closest('div.tab-pane');
        if (!tab.length) {
            return false;
        }
        return tab.is(":visible");
    }

    _onUIChange () {
        var value = null;
        if (this._geometry) {
            value = this.format.writeGeometry(this._geometry);
        }
        this._setValue(value, false);
    }

    _setupControls () {

        /* Add a draw interaction depending on geoType of the field
         * plus adds a modify interaction to be able to change line
         * and polygons.
         * As modify needs to get pointer position on map it requires
         * the map to be rendered before being created
         */
        var handler = null;
        if (this.geoType === 'POLYGON') {
            handler = "Polygon";
        } else if (this.geoType === 'MULTIPOLYGON') {
            handler = "MultiPolygon";
        } else if (this.geoType === 'LINESTRING') {
            handler = "LineString";
        } else if (this.geoType === 'MULTILINESTRING') {
            handler = "MultiLineString";
        } else if (this.geoType === 'POINT') {
            handler = "Point";
        } else if (this.geoType === 'MULTIPOINT') {
            handler = "MultiPoint";
        } else {
            // FIXME: unsupported geo type
        }

        var drawControl = function (options) {
            ol.interaction.Draw.call(this, options);
        };
        inherits(drawControl, ol.interaction.Draw);
        // drawControl.prototype = Object.create(ol.interaction.Draw.prototype);
        // drawControl.prototype.constructor = drawControl;
        drawControl.prototype.finishDrawing = function () {
            this.source_.clear();
            ol.interaction.Draw.prototype.finishDrawing.call(this);
        };

        this.drawControl = new drawControl({
            source: this.source,
            type: handler,
        });
        this.map.addInteraction(this.drawControl);
        var onchange_geom = function (e) {
            // Trigger onchanges when drawing is done
            if (e.type === 'drawend') {
                this._geometry = e.feature.getGeometry();
            } else {
                // Modify end
                this._geometry = e.features.item(0).getGeometry();
            }
            this._onUIChange();
        }.bind(this);
        this.drawControl.on('drawend', onchange_geom);

        this.features = this.source.getFeaturesCollection();
        this.modifyControl = new ol.interaction.Modify({
            features: this.features,
            // The SHIFT key must be pressed to delete vertices, so
            // that new vertices can be drawn at the same position
            // of existing vertices
            deleteCondition: function (event) {
                return ol.events.condition.shiftKeyOnly(event) &&
                  ol.events.condition.singleClick(event);
            },
        });
        this.map.addInteraction(this.modifyControl);
        this.modifyControl.on('modifyend', onchange_geom);

        var self = this;
        var ClearMapControl = function (opt_options) {
            var options = opt_options || {};
            var button = document.createElement('button');
            button.innerHTML = '<i class="fa fa-trash"/>';
            button.addEventListener('click', function () {
                self.source.clear();
                self._geometry = null;
                self._onUIChange();
            });
            var element = document.createElement('div');
            element.className = 'ol-clear ol-unselectable ol-control';
            element.appendChild(button);

            ol.control.Control.call(this, {
                element: element,
                target: options.target,
            });
        };
        inherits(ClearMapControl, ol.control.Control);
        // ClearMapControl.prototype = Object.create(ol.control.Control.prototype);
        // ClearMapControl.prototype.constructor = ClearMapControl;
        this.clearmapControl = new ClearMapControl();
        this.map.addControl(this.clearmapControl);
    }

    _renderMap () {
        if (!this.map) {
            // var $el = this.$el[0];
            console.log(this)
            $(this.__owl__.parent.bdom.el).css({width: '100%', height: '100%'});
            this.map = new ol.Map({
                layers: this.rasterLayers,
                target: $(this.__owl__.bdom.el)[0],
                view: new ol.View({
                    center: [0, 0],
                    zoom: 5,
                }),
            });
            this.map.addLayer(this.vectorLayer);

            this.format = new ol.format.GeoJSON({
                internalProjection: this.map.getView().getProjection(),
                externalProjection: 'EPSG:' + this.srid,
            });

            $(document).trigger('FieldGeoEngineEditMap:ready', [this.map]);
            this._setValue(this.value);

            // if (this.mode !== 'readonly' &&
                // !this.get('effective_readonly')) {
                this._setupControls();
                this.drawControl.setActive(true);
                this.modifyControl.setActive(true);
                this.clearmapControl.element.children[0].disabled = false;
            // }
        }
    }

    _render () {
        console.log(this.props.record.resModel)
        console.log(this.props.name)
        // debugger;

        this.env.services.rpc("/web/dataset/call_kw", {
            model: this.props.record.resModel,
            method: "get_edit_info_for_geo_column",
            kwargs: {
            },
            args: [
                this.props.name
            ],
        })
        // this.env.services.rpc({
        //     model: this.props.record.resModel,
        //     method: 'get_edit_info_for_geo_column',
        //     // args: [this.props.name],
        //     args: [[], {
        //         column: this.props.name
        //     }]
        // })
        .then(function (result) {
            this._createLayers(result);
            this.geoType = result.geo_type;
            this.projection = result.projection;
            this.defaultExtent = result.default_extent;
            this.defaultZoom = result.default_zoom;
            this.restrictedExtent = result.restricted_extent;
            this.srid = result.srid;
            //if (this.$el.is(":visible") || this._isTabVisible()) {
                this._renderMap();
            //}
        }.bind(this));
    }

}

FieldGeoEngineEditMapOwl.template = "FieldGeoEngineEditMapOwl";
FieldGeoEngineEditMapOwl.props = standardFieldProps;

registry.category("fields").add("geo_edit_map", FieldGeoEngineEditMap);
registry.category("fields").add("geo_edit_map_owl", FieldGeoEngineEditMapOwl);
view_registry.add('activity', GeoengineView);