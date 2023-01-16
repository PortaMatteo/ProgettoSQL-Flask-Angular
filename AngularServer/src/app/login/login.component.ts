import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email:string = '';
  passw:string = '';
  url:string = "https://3245-portamatteo-progettosql-zv55c5d5uao.ws-eu82.gitpod.io/login/data"
  constructor(public http: HttpClient) {
  }

  onSubmit(data){
    console.log(data)
    /**this.http.post(this.url,{email:email,password:passw}).subscribe(res => {
      console.log(res)
      ///sessionStorage.setItem('username',res[0].username)
      ///sessionStorage.setItem('id',res[0].id)
      });*/
  }
}
