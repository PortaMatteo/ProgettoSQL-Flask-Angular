import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-like',
  templateUrl: './like.component.html',
  styleUrls: ['./like.component.css']
})
export class LikeComponent {
  url: string = "https://3245-portamatteo-progettosql-ath3c3g4ev5.ws-eu83.gitpod.io/liked"
  id_u = sessionStorage.getItem('id')
  tracks!:any;
  url3: string = "https://3245-portamatteo-progettosql-ath3c3g4ev5.ws-eu83.gitpod.io/dislike"
  username = sessionStorage.getItem('username');
  constructor(public http: HttpClient,private router: Router){
    if (sessionStorage.getItem('id') != null){
      this.get(this.url + "?id=" + this.id_u)
    }
    else{
      this.router.navigate(['/home'])
    };
  }
  get(url: string): void {
    this.http.get(url).subscribe(res => {
      this.tracks=res
    });
  }
  dislike(data){
    this.http.post(this.url3,{id_t:data,id_u:this.id_u}).subscribe(res => {});
    window.location.reload()
  }
}
