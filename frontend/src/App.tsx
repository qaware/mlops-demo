import * as React from 'react';
import Header from './components/Header';
import Content from './components/Content';
import Footer from './components/Footer';

/**
 * The app.
 * @constructor
 */
export default function App() {
    return (
        <>
            <Header/>
            <Content/>
            <Footer/>
        </>
    );
}
