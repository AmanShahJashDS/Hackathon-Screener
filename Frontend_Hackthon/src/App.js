import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../src/Components/Header';
import Footer from '../src/Components/Footer';

function App() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh', // Use full viewport height
    }}>
      <Header />
      <main style={{
        flex: '1 0 auto',
        padding: '50px',
        marginTop: '64px', // Assuming header height
      }}>
        {/* Outlet to render nested routes */}
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

export default App;
