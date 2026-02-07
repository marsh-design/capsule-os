import { Link, useLocation } from "react-router-dom"

export default function Layout({ children }) {
  const location = useLocation()

  const linkClass = (path) =>
    `text-[11px] font-medium tracking-wide uppercase transition-colors duration-200 ${
      location.pathname === path
        ? "text-black border-b border-black pb-px"
        : "text-neutral-500 hover:text-black"
    }`

  return (
    <div className="min-h-screen bg-offwhite">
      <header className="sticky top-0 z-50 bg-offwhite/95 backdrop-blur border-b border-stone-200">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-10">
          <nav className="flex justify-between items-center h-16 md:h-20">
            <Link
              to="/"
              className="font-serif text-2xl md:text-3xl font-medium tracking-tight text-black hover:opacity-80 transition-opacity"
            >
              CapsuleOS
            </Link>
            <div className="flex items-center gap-8">
              <Link to="/" className={linkClass("/")}>
                Plan
              </Link>
              <Link to="/capsule" className={linkClass("/capsule")}>
                Capsule
              </Link>
              <Link to="/browse" className={linkClass("/browse")}>
                Browse
              </Link>
              <Link to="/scanner" className={linkClass("/scanner")}>
                Should I Buy
              </Link>
            </div>
          </nav>
        </div>
      </header>
      <main className="max-w-[1400px] mx-auto px-6 lg:px-10 py-12 md:py-16">
        {children}
      </main>
    </div>
  )
}
