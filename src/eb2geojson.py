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


def get_id_name(str_in: str):
    str_out = ''
    try:
        str_out = str_in.replace("CompressorStation", "CS_")
    except Exception as e:
        print(f"get_title_from_html_div {str_in}. Exception occurred {str(e)}")
        if len(str_in):
            str_out = str_in
    return str_out


def get_title_from_html_div(str_in: str):
    str_out = ''
    try:
        soup = BeautifulSoup(str_in, 'html.parser')
        str_out = soup.get_text().strip()
    except Exception as e:
        print(f"get_title_from_html_div {str_in}. Exception occurred {str(e)}")
        if len(str_in):
            str_out = str_in
    return str_out


def get_href_from_html_div(str_in: str):
    str_out = ''
    try:
        soup = BeautifulSoup(str_in, 'html.parser')
        soup1 = soup.find('a')
        str_out = soup1['href']
    except Exception as e:
        print(f"get_href_from_html_div {str_in}. Exception occurred {str(e)}")

    return str_out


def get_href_from_html_img(str_in: str):
    str_out = ''
    try:
        soup = BeautifulSoup(str_in, 'html.parser')
        soup1 = soup.find('img')
        str_out = soup1['src']
    except Exception as e:
        print(f"get_href_from_html_img {str_in}. Exception occurred {str(e)}")
    return str_out


def get_alt_from_html_img(str_in: str):
    str_out = ''
    try:
        soup = BeautifulSoup(str_in, 'html.parser')
        soup1 = soup.find('img')
        str_out = soup1['alt'].replace('&quot;', '')
    except Exception as e:
        print(f"get_alt_from_html_img {str_in}. Exception occurred {str(e)}")
    return str_out


def get_dir_from_table(str_in: str):
    str_out = ''
    try:
        soup = BeautifulSoup(str_in, 'html.parser')
        # soup1 = soup.find('table').find('tr').find('td')
        soup2 = soup.find_all('td')

        for soup_current in soup2:
            str_tmp = soup_current.contents[0]
            if str_tmp.lower().startswith("направление"):
                str_out = str_tmp
    except Exception as e:
        print(f"get_href_from_html_div {str_in}. Exception occurred {str(e)}")
        if len(str_in):
            str_out = "нет данных"
    return str_out


def get_dir_href_from_table(str_in: str):
    str_out = ''
    try:
        soup = BeautifulSoup(str_in, 'html.parser')
        soup1 = soup.find('table').find('tr').find('a')
        str_out = soup1['href']
    except Exception as e:
        print(f"get_href_from_html_div {str_in}. Exception occurred {str(e)}")
        if len(str_in):
            str_out = "нет данных"
    return str_out


def get_dir_text_from_table(str_in: str):
    str_out = ''
    try:
        soup = BeautifulSoup(str_in, 'html.parser')
        soup1 = soup.find('table').find('tr').find('a')
        str_out = soup1.contents[0]
    except Exception as e:
        print(f"get_href_from_html_div {str_in}. Exception occurred {str(e)}")
        if len(str_in):
            str_out = "нет данных"
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
            #  Обрабатываем заголовок (тот html, который там находится)
            html_header = gdf['balloonContentHeader'].iloc[i]

            gdf.loc[i, 'id_name'] = get_id_name(gdf['id'].iloc[i])
            gdf.loc[i, 'title'] = get_title_from_html_div(html_header)
            gdf.loc[i, 'title_href'] = get_href_from_html_div(html_header)
            gdf.loc[i, 'img_href'] = get_href_from_html_img(html_header)
            gdf.loc[i, 'img_alt'] = get_alt_from_html_img(html_header)

            #  Обрабатываем body (тот html, который там находится)
            html_body = gdf['balloonContentBody'].iloc[i]
            # Направление
            gdf.loc[i, 'dir'] = get_dir_from_table(html_body)
            gdf.loc[i, 'dir_href'] = get_dir_href_from_table(html_body)
            gdf.loc[i, 'dir_text'] = get_dir_text_from_table(html_body)



            str_temp = gdf.loc[i, 'dir']
            print(f"{i} as {str_temp}")

        # Меняем координаты местами
        gdf1 = geopandas.GeoDataFrame(
            gdf, geometry=geopandas.points_from_xy(gdf.geometry.y, gdf.geometry.x), crs="EPSG:4326"
        )
        gdf1 = gdf1.rename(columns={'iconImageHref': 'icon_href'})
        gdf1 = gdf1.rename(columns={'clusterCaption': 'name_ru'})
        gdf1.to_file(file_geojson_out, driver='GeoJSON')

        # for i in range(0, len(gdf)):
        #     _lon = gdf.geometry.x.iloc[i]
        #     _lat = gdf.geometry.y.iloc[i]
        #     gdf.loc[i, 'lon'] = _lon
        #     gdf.loc[i, 'lat'] = _lat
        #     gdf.geometry.x.iloc[i] = _lat
        #     gdf.geometry.y.iloc[i] = _lon

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
