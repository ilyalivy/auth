import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';
import OrganizationCreation from './components/OrganizationCreation';
import AddUser from './components/AddUser';
import Nav from './components/Nav';
import Organizations from './components/Organizations';


function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/org-creation" element={<OrganizationCreation />} />
        <Route path="/add-user" element={<AddUser />} />
        <Route path="/organizations" element={<Organizations />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
