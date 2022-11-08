import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from 'src/app/services/login.service';
import { Usuario } from 'src/app/interfaces/usuario';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  form_register:FormGroup;
  form_login:FormGroup;
  Usuario:Usuario;
  flag_register:boolean;
  flag_login:boolean;

  constructor(public fb_register:FormBuilder, public fb_login:FormBuilder, private http:LoginService) {
    this.form_register = this.fb_register.group({
      email_r: ["", [Validators.required, Validators.email]],
      nombre: ["", [Validators.required]],
      password_r: ["", [Validators.required, Validators.minLength(8)]]
    });
    
    this.form_login = this.fb_login.group({
      email_l: ["", [Validators.required, Validators.email]],
      password_l: ["", [Validators.required]]
    });
    
    this.Usuario = {
      id_usuario: 0,
      nombre: '',
      email: ''
    }
    
    this.flag_register = false;
    this.flag_login = false;
  }

  
  ngOnInit(): void {
  }
  
  getUser(email:string):any {
    this.http.GetUsuario(email).subscribe(datos => {
      return datos[0];
    })
  }
  
  async onSubmitRegister() {
    if (this.form_register.valid && this.form_register.get('email_r')?.valid) {
      const nombre = this.form_register.get('nombre')?.value;
      const password = this.form_register.get('password_r')?.value;
      const email = this.form_register.get('email_r')?.value;
      
      await this.http.GetUsuario(email).subscribe(datos => {
        if(typeof(datos[0]) === 'undefined') {
          this.flag_register = false;
          this.http.PostUsuario(nombre, password, email).subscribe();
          this.http.GetUsuario(email).subscribe(datos => {this.Usuario = datos[0]})
        } else {
          this.flag_register = true;
        }
      })
    }
  }
 
  async onSubmitLogin() {
    if (this.form_login.valid && this.form_login.get('email_l')?.valid) {
      const email = this.form_login.get('email_l')?.value;
      const password = this.form_login.get('password_l')?.value;
        
      await this.http.PostLogin(email, password);
        
      if (this.http.isLoggedIn) {
        this.Usuario = this.http.currentUser;
      }
    }
  }

  isLoggedIn():boolean {
    return this.http.isLoggedIn;
  }
  
}
