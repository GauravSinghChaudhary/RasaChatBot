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
  cancelUrl:string = "http://localhost:5000?stop=yes";
  constructor(public http: HttpClient) {
    console.log('Hello RestProvider Provider');
  }
  requestData() {

        return new Promise(resolve => {
              this.http.get(this.apiUrl).subscribe(data => {
                resolve(data);
              }, err => {
                console.log(err);
              });

      });
    }

    cancelRequest() {

            return new Promise(resolve => {
                  this.http.get(this.cancelUrl).subscribe(data => {
                    resolve(data);
                  }, err => {
                    console.log(err);
                  });

          });
        }
}
