import { Chart } from './../models/chart.model';
import { SearchTerm } from './../models/search-term.model';
import { TweetPieChart } from './../models/tweet-pie-chart.model';
import { Injectable } from '@angular/core';
import { Tweet } from '../models/tweet.model';
import { Observable } from 'rxjs';
import { AppConfig } from 'src/app/app-config';
import { HttpClient } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class TwitterSearchService {
    
    private urlGetTweets = '/gettweets';
    private urlGetPieChart = '/getpiechart';
    private urlGetTopSearches = '/gettopterms';
    private urlGetLiveTest = '/getlivetest';
    private urlGetDashboardData = '/getDashboardData';
    private urlCreateSentimentJob = '/createSentimentJob';
    myTweet: Tweet;


    constructor(private http: HttpClient) { }

    getTweets(searchTerm: string): Observable<Tweet[]> {
        return this.http.get<Tweet[]>(`${AppConfig.API_ENDPOINT}${this.urlGetTweets}?text=${searchTerm}`);
    }

    getPieChart(searchTerm: string, useTimeFilter: Boolean, dateSince: string, dateUntil: string): Observable<TweetPieChart[]> {
        console.log(`${AppConfig.API_ENDPOINT}${this.urlGetPieChart}?text=${searchTerm}&count=1000`);
        if (useTimeFilter)
            return this.http.get<TweetPieChart[]>(`${AppConfig.API_ENDPOINT}${this.urlGetPieChart}?text=${searchTerm}&useTimeFilter=${useTimeFilter}&dateSince=${dateSince}&dateUntil=${dateUntil}&count=1000`);
        else
            return this.http.get<TweetPieChart[]>(`${AppConfig.API_ENDPOINT}${this.urlGetPieChart}?text=${searchTerm}&useTimeFilter=${useTimeFilter}&count=1000`);
    }

    getTopSearches(): Observable<SearchTerm[]> {
        return this.http.get<SearchTerm[]>(`${AppConfig.API_ENDPOINT}${this.urlGetTopSearches}`);
    }

    getLiveTest(searchTerm: string): Observable<number> {
        return this.http.get<number>(`${AppConfig.API_ENDPOINT}${this.urlGetLiveTest}?text=${searchTerm}`);
    }

    getDashboard(): Observable<Chart[]> {
        return this.http.get<Chart[]>(`${AppConfig.API_ENDPOINT}${this.urlGetDashboardData}`);
    }

    createSentimentJob(searchTerm: string, startDateString:string, intervalSelect: string) : Observable<string>{
        // return this.http.get<string>(`${AppConfig.API_ENDPOINT}${this.urlCreateSentimentJob}?text=${searchTerm}&startDate=${dt}&interval=${intervalSelect}`);
        return this.http.get<string>(`${AppConfig.API_ENDPOINT}${this.urlCreateSentimentJob}?text=${searchTerm}&startDate=${startDateString}&interval=${intervalSelect}`);
    }
}
