import React,{useState} from 'react';
import axios from "axios";
import {Form,Button,Container} from "react-bootstrap";
import {Redirect} from "react-router-dom";

export default function Login() {
    const [email,setEmail]=useState(null)
    const [password,setPassword]=useState(null)
    const [msg,setMsg]=useState(null)
    const [error,setError]=useState(null)

    const login=()=>{
        axios.post("http://localhost:8000/api/login",{
            email,password
        }).then(
            res=>{
                console.log(res.data);
                sessionStorage.setItem('email',res.data.email);
                setError(null)
                setMsg("Logged in successfully")
            }
        ).catch(error=>{
            console.log(error.response.data.msg)
            setMsg(null)
            setError(error.response.data.msg)
        })
    }

    const register=()=>{
        axios.post("http://localhost:8000/api/register",{
            email,password
        }).then(
            res=>{
                console.log(res.data);
                setMsg("Registered successfully");
                setError(null);
            }
        ).catch(error=>{
            console.log(error.response.data.msg)
            setMsg(null)
            setError(error.response.data.msg)
        })
    }
    if(sessionStorage.getItem('email'))
        return(<Redirect  to={{pathname:"/events"}}/>)
    return (
        <Container>
        <h3>Welcome</h3>
            <Form className="mt-5">
            <Form.Group controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email" onChange={(e)=>{setEmail(e.target.value)}}/>
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" onChange={(e)=>{setPassword(e.target.value)}}/>
            </Form.Group>
            <h6 style={{color:"green"}}>{msg}</h6>
            <h6 style={{color:"red"}}>{error}</h6>
            <Button variant="success" onClick={login}>
                Login
            </Button>
            <Button className="ml-5" variant="primary" onClick={register} >
                Register
            </Button>
            </Form>
            </Container>
    )
}
