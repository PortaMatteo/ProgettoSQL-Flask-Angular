import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  @Input() url : string = "https://3245-portamatteo-progettosql-ep8zc3nv5w0.ws-eu78.gitpod.io/register/data";
}
