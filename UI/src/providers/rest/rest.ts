import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

/*
  Generated class for the RestProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class RestProvider {
  apiUrl:string = "http://localhost:5000/";
  constructor(public http: HttpClient) {
    console.log('Hello RestProvider Provider');
  }
  requestData() {

        this.http.get(this.apiUrl).subscribe(() => {
                                          console.log("rest");
                                        }, err => {
                                          console.log(err);
                                        });

    }
}
