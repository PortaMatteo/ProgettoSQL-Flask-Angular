import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  search!: any;
  loading!: Boolean;
  url: string = "https://3245-portamatteo-progettosql-7mw9jyajuwk.ws-eu77.gitpod.io/home";

  constructor(public http: HttpClient) {
    this.get(this.url);
  }

  get(url: string): void {
    this.loading = true;
    this.http.get(url).subscribe(data => {
      this.search = data;
      this.loading = false;
    });
  }

  onKey(value: string) {
    this.get(this.url + "?search=" + value);
  }
}
