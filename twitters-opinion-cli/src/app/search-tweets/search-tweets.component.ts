import { TweetPieChart } from './../shared/models/tweet-pie-chart.model';
import { Tweet } from './../shared/models/tweet.model';
import { TwitterSearchService } from './../shared/services/twitter-search.service';
import { Component, OnInit, Input, ViewChild, TemplateRef } from '@angular/core';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgbModal, ModalDismissReasons, NgbModalOptions } from '@ng-bootstrap/ng-bootstrap';
import { Inject, Injectable } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { Chart } from './../shared/models/chart.model';

@Component({
    selector: 'app-search-tweets',
    templateUrl: './search-tweets.component.html',
    styleUrls: ['./search-tweets.component.css']
})
export class SearchTweetsComponent implements OnInit {

    tweets: Tweet[] = [];
    tweetCount: number;
    chartData: TweetPieChart[] = [];
    showModalBox: boolean = true;
    showLabel: boolean;
    dateSince: string = null;
    dateUntil: string = null;
    useTimeFilter: Boolean = false;
    @ViewChild('modalBoxPos') modalBoxPos: any;
    @ViewChild('modalBoxNeg') modalBoxNeg: any;
    @ViewChild('modalBoxNeu') modalBoxNeu: any;
    @Input() query: string;

    constructor(private router: Router, private service: TwitterSearchService, private route: ActivatedRoute, private SpinnerService: NgxSpinnerService, private modalService: NgbModal, @Inject(DOCUMENT) private document: Document) { }

    ngOnInit(): void {
        // this.getTweets("trump");
        // this.createChart();
        this.showLabel = false;
        this.route.queryParams.subscribe(params => {
            this.query = params['query'];
            this.useTimeFilter = params['useTimeFilter'];
            this.dateSince = params['dateSince'];
            this.dateUntil = params['dateUntil'];
            console.log("Ovo je: " + this.dateSince + " " + this.dateUntil);
            this.getPieChart(this.query, this.useTimeFilter, this.dateSince, this.dateUntil);
        });

    }

    open(content) {
        let options: NgbModalOptions = {
            size: 'xl'
        };

        this.modalService.open(content, options);
    }

    closeModal() {
        this.modalService.dismissAll();
    }

    getTweets(searchTerm: string) {
        this.service.getTweets(searchTerm).subscribe(
            res => {
                this.tweets = res;
                this.tweetCount = this.tweets.length;
            },
            err => {
                console.log(err);
            }
        );
        console.log(this.tweets);
    }

    getPieChart(searchTerm: string, useTimeFilter: Boolean, dateSince: string, dateUntil: string) {
        this.SpinnerService.show();
        this.service.getPieChart(searchTerm, useTimeFilter, dateSince, dateUntil).subscribe(
            res => {
                this.chartData = res;
                // console.log(this.chartData);
                this.SpinnerService.hide();
                this.showLabel = true;
                this.createChart();
            },
            err => {
                this.SpinnerService.hide();
                this.router.navigateByUrl(`/search`)
                alert(err.error.message)
                console.log(err);
            }
        );

    }

    createChart() {
        let chart = am4core.create("chartdiv", am4charts.PieChart);
        chart.data = this.chartData;

        // Add and configure Series
        let pieSeries = chart.series.push(new am4charts.PieSeries());
        pieSeries.tooltip.label.interactionsEnabled = true;
        pieSeries.tooltip.keepTargetHover = true;
        // pieSeries.tooltip.events.on("hit", function (ev) {
        //     console.log("clicked on ", ev.target);
        //     // this.showModalBox = true;
        //     console.log(pieSeries.dataProvider.group.content);
        //     let tweetPieChart = ev.target.dataItem.dataContext as TweetPieChart;
        //     if (tweetPieChart.label.includes("Pozitivni")) {
        //         this.open(this.modalBoxPos);
        //     } else if (tweetPieChart.label.includes("Negativni")) {
        //         this.open(this.modalBoxNeg);
        //     } else {
        //         this.open(this.modalBoxNeu);
        //     }
        // }, this);
        var colorSet = new am4core.ColorSet();
        colorSet.list = ["#00f147", "#008984", "#ffce00", "#c23854",  "#d20000"].map(function (color) {
            return am4core.color(color);
        });
        pieSeries.colors = colorSet;
        pieSeries.dataFields.value = "num";
        pieSeries.dataFields.category = "label";
    }

}
