import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-playlist-dot',
  templateUrl: './playlist-dot.component.html',
  styleUrls: ['./playlist-dot.component.css']
})
export class PlaylistDotComponent {
  id!:any;
  plylst!:any;
  username = sessionStorage.getItem('username');
  url2: string = "https://3245-portamatteo-progettosql-nyjfa3kgy7b.ws-eu83.gitpod.io/deletetrack"
  constructor(private activatedRoute: ActivatedRoute,public http: HttpClient,private router: Router) {
    if (sessionStorage.getItem('id') == null){
      this.router.navigate(['/home'])
    }
  }
  ngOnInit() {
    this.activatedRoute.params.subscribe(paramsId => {
        this.id = paramsId['p'];
    });
    this.http.get("https://3245-portamatteo-progettosql-nyjfa3kgy7b.ws-eu83.gitpod.io/playlistview" + "?id=" + this.id).subscribe(res=>{
      this.plylst = res
    })
  }

  deletetrack(data){
    this.http.post(this.url2,{id_t:data,id_p:this.id}).subscribe(res => {});
    window.location.reload()
  }
}
