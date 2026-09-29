import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

// Layout for public pages: Home, About, Login, Register
const PublicLayout = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 pt-16">
        {children}
      </main>
      <Footer />
    </div>
  )
}

export default PublicLayout
