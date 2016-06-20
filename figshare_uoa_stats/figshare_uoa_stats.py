# -*- coding: utf-8 -*-
from pigshare.api import figshare_api
from pigshare.stats_api import figshare_stats_api
from influxdb import InfluxDBClient
import pprint

class figshare_stats:

    def __init__(self, stats_token, figshare_api_token, institution="auckland", influxdb_host, influxdb_port=8086, influxdb_db="figshare"):

        self.stats_api = figshare_stats_api(institution=institution, stats_token)
        self.api = figshare_api(token=figshare_api_token)
        self.influxdb = InfluxDBClient(host=influxdb_host, port=influxdb_port, database=influxdb_db)

    def get_all_articles(self):

        articles = self.api.call_list_institution_articles(12)

        result = {}
        for a in articles:
            result[a.id] = {}
            article = self.api.call_read_article(a.id)
            result[a.id]['article'] = article

        return result

    def get_all_views(self, articles):

        for a in articles.keys():
            views = self.stats_api.call_get_total_article_views(a)
            for key, value in views.items():
                totals = value['totals']
                articles[a]['views'] = totals

    def get_all_downloads(self, articles):

        for a in articles.keys():
            downloads = self.stats_api.call_get_total_article_downloads(a)
            for key, value in downloads.items():
                totals = value['totals']
                articles[a]['downloads'] = totals


    def get_current_data(self):

        articles = self.get_all_articles()
        articles = articles[0:2]
        self.get_all_views(articles)
        self.get_all_downloads(articles)

        return articles


    def get_timeline_all_articles(self, articles):

        day_stats = {}
        article_stats = {}

        for a in articles.keys():

            article_stats[a] = {}

            timeline_views = self.stats_api.call_get_timeline_article_views(a, granularity="day", start_date="1970-01-01", end_date="2016-06-13")
            for key, value in timeline_views.items():
                if value.get('timeline', None):
                    for day, views in value['timeline'].items():

                        if not article_stats[a].get(day, None):
                            article_stats[a][day] = {}

                        article_stats[a][day]['views'] = views

            timeline_downloads = self.stats_api.call_get_timeline_article_downloads(a, granularity="day", start_date="1970-01-01", end_date="2016-06-13")
            for key, value in timeline_downloads.items():
                if value.get('timeline', None):
                    for day, downloads in value['timeline'].items():

                        if not article_stats[a].get(day, None):
                            article_stats[a][day] = {}

                        article_stats[a][day]['downloads'] = downloads

        total_author_views = {}
        total_author_downloads = {}
        total_category_views = {}
        total_category_downloads = {}

        article_total_views_temp = 0
        article_total_downloads_temp = 0


        for article_id, stats in article_stats.items():

            article = articles[article_id]

            total_views = 0
            total_downloads = 0
            for day in sorted(stats.keys()):

                views = stats[day].get('views', 0)
                downloads = stats[day].get('downloads', 0)

                total_views = total_views + views
                total_downloads = total_downloads + downloads

                if not day_stats.get(day, None):
                    day_stats[day] = {}
                    day_stats[day]['articles'] = {}
                    day_stats[day]['categories'] = {}
                    day_stats[day]['authors'] = {}


                day_stats[day]['articles'][article_id] = {}
                day_stats[day]['articles'][article_id]['total_views'] = total_views
                day_stats[day]['articles'][article_id]['total_downloads'] = total_downloads
                day_stats[day]['articles'][article_id]['views'] = views
                day_stats[day]['articles'][article_id]['downloads'] = downloads


        for day in sorted(day_stats.keys()):

            for article_id in day_stats[day]['articles'].keys():

                article = articles[article_id]['article']

                views_temp = day_stats[day]['articles'][article_id]['views']
                downloads_temp = day_stats[day]['articles'][article_id]['downloads']

                for category in article['categories']:

                    if not total_category_views.get(category.title):
                        total_category_views[category.title] = 0
                    if not total_category_downloads.get(category.title):
                        total_category_downloads[category.title] = 0

                    if not day_stats[day]['categories'].get(category.title, None):
                        day_stats[day]['categories'][category.title] = {}
                        day_stats[day]['categories'][category.title]['views'] = 0
                        day_stats[day]['categories'][category.title]['downloads'] = 0
                        day_stats[day]['categories'][category.title]['total_views'] = total_category_views[category.title]
                        day_stats[day]['categories'][category.title]['total_downloads'] = total_category_downloads[category.title]

                    total_category_views[category.title] += views_temp
                    total_category_downloads[category.title] += downloads_temp

                    day_stats[day]['categories'][category.title]['total_views'] = total_category_views[category.title]
                    day_stats[day]['categories'][category.title]['total_downloads'] = total_category_downloads[category.title]

                    day_stats[day]['categories'][category.title]['views'] += views_temp
                    day_stats[day]['categories'][category.title]['downloads'] += downloads_temp

                for author in article['authors']:

                    if not total_author_views.get(author.full_name, None):
                        total_author_views[author.full_name] = 0

                    if not total_author_downloads.get(author.full_name, None):
                        total_author_downloads[author.full_name] = 0

                    if not day_stats[day]['authors'].get(author.full_name, None):
                        day_stats[day]['authors'][author.full_name] = {}
                        day_stats[day]['authors'][author.full_name]['views'] = 0
                        day_stats[day]['authors'][author.full_name]['downloads'] = 0
                        day_stats[day]['authors'][author.full_name]['total_views'] = total_author_views[author.full_name]
                        day_stats[day]['authors'][author.full_name]['total_downloads'] = total_author_downloads[author.full_name]

                    total_author_views[author.full_name] += views_temp
                    total_author_downloads[author.full_name] += downloads_temp

                    day_stats[day]['authors'][author.full_name]['total_views'] = total_author_views[author.full_name]
                    day_stats[day]['authors'][author.full_name]['total_downloads'] = total_author_downloads[author.full_name]

                    day_stats[day]['authors'][author.full_name]['views'] += views_temp
                    day_stats[day]['authors'][author.full_name]['downloads'] += downloads_temp

                if not day_stats[day].get('totals', None):
                    day_stats[day]['totals'] = {}

                article_total_views_temp += views_temp
                day_stats[day]['totals']['total_views'] = article_total_views_temp
                article_total_downloads_temp += downloads_temp
                day_stats[day]['totals']['total_downloads'] = article_total_downloads_temp


        return day_stats

    def get_timeline_data(self):

        articles = self.get_all_articles()

        day_stats = self.get_timeline_all_articles(articles)

        for day,stats in sorted(day_stats.items()):

            for article_id, stats_dict in stats['articles'].items():
                self.insert_into_influxdb(day, 'article', 'total_views', article_id, stats_dict, articles)
                self.insert_into_influxdb(day, 'article', 'total_downloads', article_id, stats_dict, articles)

            for author_name, stats_dict in stats['authors'].items():
                self.insert_into_influxdb(day, 'author', 'total_views', author_name, stats_dict, articles)
                self.insert_into_influxdb(day, 'author', 'total_downloads', author_name, stats_dict, articles)

            for category_name, stats_dict in stats['categories'].items():
                self.insert_into_influxdb(day, 'category', 'total_views', category_name, stats_dict, articles)
                self.insert_into_influxdb(day, 'category', 'total_downloads', category_name, stats_dict, articles)

            self.insert_into_influxdb(day, 'totals', 'total_views', 'total', stats['totals'], articles)
            self.insert_into_influxdb(day, 'totals', 'total_downloads', 'total', stats['totals'], articles)

    def insert_into_influxdb(self, date, category, field, item_id, stats_dict, all_articles=None):


        json_body_views = {}

        json_body_views['measurement'] = 'figshare.'+category

        json_body_views['time'] = date
        json_body_views['fields'] = {}
        json_body_views['fields'][field] = stats_dict.get(field, 0)

        json_body_views['tags'] = {}
        json_body_views['tags']['id'] = item_id
        # json_body_views['tags']['stats_type'] = field

        self.influxdb.write_points([json_body_views])
