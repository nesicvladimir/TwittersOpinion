import { Chart } from './../shared/models/chart.model';
import { Component, OnInit } from '@angular/core';
import { TwitterSearchService } from '../shared/services/twitter-search.service';
import { NgbModal, NgbDateStruct, NgbCalendar, NgbTimeStruct } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

    constructor(private service: TwitterSearchService, private calendar: NgbCalendar, private modalService: NgbModal) {

    }
    public chartDatasets: Array<any> = [];
    searchTerm: string = '';
    interval: string = 'hour';
    public charts: Chart[] = [];
    public minDate = new Date();
    public startDate: NgbDateStruct;
    public startTime: NgbTimeStruct;
    dateNow: NgbDateStruct;
    public intervalSelect = '47';
    // public chartLabels: Array<any> = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    public chartLabels;
    ngOnInit(): void {
        this.intervalSelect = '47';
        this.service.getDashboard().subscribe(
            res => {
                this.charts = res;
                this.chartDatasets = this.charts[0].chartData;
                this.chartLabels = this.charts[0].chartLabels;
            },
            err => {
                alert(err.error.message)
                console.log(err);
            }
        );
    }

    public chartType: string = 'line';



    public chartColors: Array<any> = [
        {
            backgroundColor: 'rgba(210, 0, 0, .2)',
            borderColor: 'rgba(255, 0, 0, .7)',
            borderWidth: 2,
        },
        {
            backgroundColor: 'rgba(105, 0, 132, .2)',
            borderColor: 'rgba(200, 99, 132, .7)',
            borderWidth: 2,
        },
        {
            backgroundColor: 'rgba(255, 206, 0, .2)',
            borderColor: 'rgba(230, 206, 0, .7)',
            borderWidth: 2,
        },
        {
            backgroundColor: 'rgba(0, 137, 132, .2)',
            borderColor: 'rgba(0, 10, 130, .7)',
            borderWidth: 2,
        },
        {
            backgroundColor: 'rgba(0, 241, 71, .2)',
            borderColor: 'rgba(0, 220, 71, .7)',
            borderWidth: 2,
        }
    ];  

    public chartOptions: any = {
        responsive: true
    };
    public chartClicked(e: any): void { }
    public chartHovered(e: any): void { }
    openVerticallyCentered(content) {
        this.modalService.open(content, { centered: true});
    }
    createNewJob() {
        if (this.searchTerm === '') {
            alert("Search term is empty!");
        } else if (this.startDate === null) {
            alert("Date is incorrect!")
        } else if (this.intervalSelect === '') {
            alert("Please choose interval!")
        } else {
            var dateStartString = this.startDate.day + '-' + this.startDate.month + '-' + this.startDate.year + ' ' + this.startTime.hour + ':' + this.startTime.minute;
            this.service.createSentimentJob(this.searchTerm, dateStartString, this.interval).subscribe(
                res => {
                    this.modalService.dismissAll();
                    
                },
                err => {
                    alert(err.error.message)
                    console.log(err);
                }
            );
        }
    }

    setStartDate(newDate: NgbDateStruct) {
        this.startDate = newDate;
        // this.enableDateUntil = true;
    }
    selectToday() {
        return this.dateNow = this.calendar.getToday();
    }
}
