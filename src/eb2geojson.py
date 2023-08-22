#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Author  :   Vyacheslav Zamaraev
#   Date    :   21.09.2023
#   Desc    :   eb 2 csv

import os
from datetime import datetime
import logging

import shapely
import geopandas
# from geopandas import GeoDataFrame, GeoSeries
# from shapely.geometry import Point
from bs4 import BeautifulSoup

import cfg


# import requests
# from bs4 import BeautifulSoup
# import random
# from time import sleep


# for anchor in soup.findAll('a'):
#     print
#     anchor['href'], anchor.string
# soup = BeautifulSoup(str_in, "lxml")
# news_para = soup.find_all("div", text=True)
# for item in news_para:
#     # SPLIT WORDS, JOIN WORDS TO REMOVE EXTRA SPACES
#     str_out = (' ').join((item.text).split())


def make_geodf(df, lat_col_name='latitude', lon_col_name='longitude'):
    """
    Take a dataframe with latitude and longitude columns, and turn
    it into a geopandas df.
    """
    from geopandas import GeoDataFrame
    from geopandas import points_from_xy
    df = df.copy()
    lat = df['latitude']
    lon = df['longitude']
    return GeoDataFrame(df, geometry=points_from_xy(lon, lat))


def get_title_from_html_div(str_in: str):
    str_out = ''
    soup = BeautifulSoup(str_in, 'html.parser')
    str_out = soup.get_text().strip()
    return str_out


def get_href_from_html_div(str_in: str):
    str_out = ''
    soup = BeautifulSoup(str_in, 'html.parser')
    soup1 = soup.find('a')
    str_out = soup1['href']
    return str_out


def get_href_from_html_img(str_in: str):
    str_out = ''
    soup = BeautifulSoup(str_in, 'html.parser')
    soup1 = soup.find('img')
    str_out = soup1['src']
    return str_out


def get_alt_from_html_img(str_in: str):
    str_out = ''
    soup = BeautifulSoup(str_in, 'html.parser')
    soup1 = soup.find('img')
    str_out = soup1['alt'].replace('&quot;','\"')
    return str_out


def geojson_load():
    file_geojson_in = os.path.join(os.getcwd(), cfg.FILE_IN)
    file_geojson_out = os.path.join(os.getcwd(), "file_geojson_out.json")
    name_field = 'name_ru'
    crs_out = cfg.CRS_OUT
    if os.path.isfile(file_geojson_out):
        os.remove(file_geojson_out)
        print(f"file deleted: {file_geojson_out} ")

    try:
        gdf = geopandas.read_file(file_geojson_in, driver="GeoJSON")

        # Записываем координаты в отдельную колонку
        for i in range(0, len(gdf)):
            gdf.loc[i, 'lon'] = gdf.geometry.y.iloc[i]
            gdf.loc[i, 'lat'] = gdf.geometry.x.iloc[i]
            gdf.loc[i, 'title'] = get_title_from_html_div(gdf['balloonContentHeader'].iloc[i])
            gdf.loc[i, 'title_href'] = get_href_from_html_div(gdf['balloonContentHeader'].iloc[i])
            gdf.loc[i, 'img_href'] = get_href_from_html_img(gdf['balloonContentHeader'].iloc[i])
            gdf.loc[i, 'img_alt'] = get_alt_from_html_img(gdf['balloonContentHeader'].iloc[i])
            str_temp =  gdf.loc[i, 'img_alt']
            print(str_temp)

        # Меняем координаты местами
        gdf1 = geopandas.GeoDataFrame(
            gdf, geometry=geopandas.points_from_xy(gdf.geometry.y, gdf.geometry.x), crs="EPSG:4326"
        )

        gdf1.to_file(file_geojson_out, driver='GeoJSON')

        # gdf['coordinates'] = list(zip(gdf.geometry.y, gdf.geometry.x))
        # gdf['coordinates'] = gdf['coordinates'].apply(Point)
        # gdf = GeoDataFrame(point_data, geometry='coordinates', crs=4326)
        # gdf['coordinates'] = gdf.apply(lambda row: Point(row['y'], row['x']), axis=1)
        # gdf1 = GeoDataFrame(gdf, crs=4326)

        # gdf1.set_geometry("centroid")
        # gdf1 = gdf1.rename(columns={'centroid': 'geom'}).set_geometry('geom')
        # gdf1 = gdf1.to_crs(crs=crs_out)

        # gdf2 = gdf1.GeoSeries(gdf1['coordinates']).map(lambda polygon: shapely.ops.transform(lambda x, y: (y, x), polygon))
        # gdf1 = GeoSeries(gdf['coordinates']).map(lambda point: shapely.transform(lambda x, y: (y, x), point))
        # gdf1 = gdf

        # gdf['lon'] = gdf.point_object.x
        # gdf['lat'] = gdf.point_object.y

        # for i in range(0, len(gdf)):
        #     _lon = gdf.geometry.x.iloc[i]
        #     _lat = gdf.geometry.y.iloc[i]
        #     gdf.loc[i, 'lon'] = _lon
        #     gdf.loc[i, 'lat'] = _lat
        #     gdf.geometry.x.iloc[i] = _lat
        #     gdf.geometry.y.iloc[i] = _lon

        # gdf.set_geometry('geom', inplace=True)
        # gdf.loc[i, 'lat'] = gdf.geometry.centroid.y.iloc[i]
        # gdf.loc[i, 'lat'] = gdf.geometry.centroid.y.iloc[i]
        # gdf['geometry'] = gdf.apply(lambda row: Point(row['y'], row['x']))
        # gdf1 = GeoDataFrame(gdf, crs=4326)

        # for i in range(0, len(gdf1)):
        #     gdf1.loc[i, 'lon'] = gdf1.geometry.centroid.x.iloc[i]
        #     gdf1.loc[i, 'lat'] = gdf1.geometry.centroid.y.iloc[i]
        # # log = set_logger(settings.NGP_FILE_LOG)
        #
        # for i in range(0, len(gdf1)):
        #     str_name = str(gdf1.loc[i, name_field]).lower().encode()
        # lon=gdf1.loc[i, 'lon'],
        # lat=gdf1.loc[i, 'lat'],
        # print(gdf1.loc[i, 'name_ru'])
        # log.info(f"Total NGP count {count}")
    except Exception as e:
        print("Exception occurred " + str(e))


def Main():
    print('Start!!!')
    time1 = datetime.now()
    print(time1)

    for handler in logging.root.handlers[:]:  # Remove all handlers associated with the root logger object.
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=cfg.FILE_LOG, format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG,
                        filemode='w')  #
    logging.info(cfg.FILE_LOG)
    logging.info(time1)

    geojson_load()

    time2 = datetime.now()
    logging.info(time2)
    print(time2)
    print(time2 - time1)
    logging.info(str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    Main()
