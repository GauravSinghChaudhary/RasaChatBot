import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

import { HttpClient } from '@angular/common/http';
import { RestProvider } from '../../providers/rest/rest';
@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
  message:string;
  bdisplay:boolean = true;
  connect:boolean = false;
  constructor(public navCtrl: NavController, public http: HttpClient, public restProvider: RestProvider) {

  }
  delay(t) {
     return new Promise(function(resolve, reject) {
         setTimeout(() => {

         this.message = "Connected";
         this.connect = false;
         resolve();
         console.log('connected');
         }, t)
     });
  }
  initiateSpeech() {
      var _this = this;
      console.log("API hit");
      this.message= "Connecting ....";
      this.bdisplay = false;
      this.connect = true;
      this.restProvider.requestData().then(() => {
                                                     console.log('connecting . . . . ');
                                                     return new Promise(function(resolve, reject) {
                                                         setTimeout(() => {
                                                             console.log('seconds Timer expired!!!');
                                                             _this.message = "Connected";
                                                             _this.connect = false;
                                                             resolve();
                                                         }, 5000)
                                                     });
                                                 })
                                                 .then(() => {
                                                     console.log('REST call completed!!!');
                                                 })
      console.log("API called");

    }

  cancel(){
  console.log("cancelled");
    this.restProvider.cancelRequest().then(()=>{
      console.log("Streaming stopped");
    });
    this.message= "";
    this.bdisplay = true;
    this.connect = false;
  }
}
