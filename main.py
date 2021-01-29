import geopandas as gpd
import pandas as pd

from shapely.wkt import loads

from bokeh.models import Slider
from bokeh.models import Select
from bokeh.models import TextInput
from bokeh.models import CheckboxGroup

from gdf2bokeh import Gdf2Bokeh

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.layouts import row

from core.line_bender import LineStringBender



class MyMapBokeh(Gdf2Bokeh):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._input_geometry = loads("LineString (539988.1411 5744267.7273, 537825.0678 5735387.5105)")
        self._relative_distance_along_line_value = 0.5
        self._offset_distance_from_line_value = 50
        self._offset_position_value = 'left'
        self._smooth_status = True

        self._original_line_layer = {
            "input_wkt": self._input_geometry.wkt,
            "line_color": "blue",
            "line_width": 10,
            "legend": "my original line"
        }
        self._curve_line_layer = {
            "input_wkt": None,
            "line_color": "red",
            "line_width": 10,
            "legend": "my curved line"
        }

    def plot(self):

        self._slider_widget_distance_along_line()
        self._slider_widget_offset_distance_from_line()
        self._combobox_widget_offset_position()
        self._inputext_widget_geom()
        self._checkbox_widget_smooth_mode()

        # original line
        self.add_layer(self._original_line_layer)
        # curved line
        geom_curved = self.__build_curve_gdf()
        curve_line_layer = {**self._curve_line_layer, "input_wkt": geom_curved}
        self.add_layer(curve_line_layer)

        self._map_layout()

    def _prepare_data(self):
        geom_curve_rebuilt = self.__build_curve_gdf()
        layer_updated = {**self._curve_line_layer, "input_wkt": geom_curve_rebuilt}
        self.get_bokeh_layer_containers[layer_updated["legend"]].data = self.refresh_existing_layer(layer_updated)

    def _slider_widget_distance_along_line(self):
        self.slider_widget_distance_along_line = Slider(start=0.1, end=1, value=0.5, step=0.1, title="Relative distance along line")
        self.slider_widget_distance_along_line.on_change('value', self.__slider_widget_distance_along_line_update)

    def __slider_widget_distance_along_line_update(self, attrname, old_value, relative_distance_along_line_value):
        self._relative_distance_along_line_value = relative_distance_along_line_value
        self._prepare_data()

    def _slider_widget_offset_distance_from_line(self):
        self.slider_widget_offset_distance_from_line = Slider(start=1, end=10000, value=1, step=500, title="offset distance from line")
        self.slider_widget_offset_distance_from_line.on_change('value', self.__slider_widget_offset_distance_from_line_update)

    def __slider_widget_offset_distance_from_line_update(self, attrname, old_value, offset_distance_from_line_value):
        self._offset_distance_from_line_value = offset_distance_from_line_value
        self._prepare_data()

    def _combobox_widget_offset_position(self):
        self.combobox_widget_offset_position = Select(title="Offset position:", value="left", options=["left", "right"])
        self.combobox_widget_offset_position.on_change('value', self.__combobox_widget_offset_position_update)

    def __combobox_widget_offset_position_update(self, attrname, old_value, offset_position_value):
        self._offset_position_value = offset_position_value
        self._prepare_data()

    def _inputext_widget_geom(self):
        self.inputext_widget_geom = TextInput(value="LineString (539988.1411 5744267.7273, 537825.0678 5735387.5105)", title="WKT geom:")
        self.inputext_widget_geom.on_change('value', self.__inputext_widget_geom_update)

    def __inputext_widget_geom_update(self, attrname, old_value, geom_value):
        self._input_geometry = loads(geom_value)
        self._prepare_data()

    def _checkbox_widget_smooth_mode(self):
        self.checkbox_curve_smooth = CheckboxGroup(labels=["Smooth"], active=[0])
        self.checkbox_curve_smooth.on_click(self.__checkbox_widget_smooth_update)

    def __checkbox_widget_smooth_update(self, smooth_status):
        self._smooth_status = False
        if len(smooth_status) == 1:
            self._smooth_status = True
        self._prepare_data()


    def __build_curve_gdf(self):
        curve_process = LineStringBender(
            self._input_geometry,
            self._relative_distance_along_line_value,
            self._offset_distance_from_line_value,
            self._offset_position_value
        )
        if self._smooth_status:
            curve_geom = curve_process.smooth_curve_geom().wkt
        else:
            curve_geom = curve_process.raw_curve_geom().wkt

        return curve_geom

    def _map_layout(self):
        layout = column(
            row(self.figure),
            row(self.inputext_widget_geom),
            row(self.checkbox_curve_smooth),
            row(self.slider_widget_distance_along_line),
            row(self.slider_widget_offset_distance_from_line),
            row(self.combobox_widget_offset_position)
        )
        curdoc().add_root(layout)
        curdoc().title = "LineString Bender"


bounds = (529957.0264, 5732815.3399, 553537.8496, 5746956.1901)
MyMapBokeh(
    title="The LineString Bender",
    width=640,
    height=800,
    x_range=(bounds[0] , bounds[2]),
    y_range=(bounds[1] , bounds[-1]),
    background_map_name="STAMEN_TONER"
).plot()
