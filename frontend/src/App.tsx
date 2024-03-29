import * as React from 'react';
import Header from './components/Header';
import Content from './components/Content';
import Footer from './components/Footer';
import {useEffect} from "react";
import {getStatus} from "./service/BackendService";
import {ThemeProvider} from "@mui/material/styles";
import theme from "./theme";
import './fonts.css';


let intervalID: string | number | NodeJS.Timeout | undefined;
/**
 * The app.
 * @constructor
 */
export default function App() {

    useEffect(()=>{
        intervalID = setInterval(() => {
            getStatus()
        }, 10000);
    }, [])

    return (
        <>
            <ThemeProvider theme={theme}>
                <Header/>
                <Content/>
                <Footer/>
            </ThemeProvider>
        </>
    );
}

export function stopInterval() {
    clearInterval(intervalID)
}
