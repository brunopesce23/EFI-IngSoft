"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Calendar, Plane, Users, MapPin, Clock, Star, Search, Plus, BarChart3 } from "lucide-react"

// Datos de ejemplo
const vuelosDestacados = [
  {
    id: 1,
    origen: "Madrid",
    destino: "Barcelona",
    fecha: "2024-01-15",
    hora: "08:30",
    precio: 89,
    disponibles: 45,
    total: 180,
    estado: "Programado",
  },
  {
    id: 2,
    origen: "Barcelona",
    destino: "Valencia",
    fecha: "2024-01-15",
    hora: "14:20",
    precio: 65,
    disponibles: 23,
    total: 150,
    estado: "Programado",
  },
  {
    id: 3,
    origen: "Madrid",
    destino: "Sevilla",
    fecha: "2024-01-16",
    hora: "11:15",
    precio: 75,
    disponibles: 67,
    total: 180,
    estado: "Programado",
  },
]

const estadisticas = {
  vuelosHoy: 24,
  pasajerosTotal: 1847,
  reservasActivas: 156,
  ocupacionPromedio: 78,
}

export default function HomePage() {
  const [busqueda, setBusqueda] = useState({
    origen: "",
    destino: "",
    fecha: "",
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Plane className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">AeroGestión</h1>
                <p className="text-sm text-gray-500">Sistema de Gestión de Aerolínea</p>
              </div>
            </div>
            <nav className="hidden md:flex space-x-6">
              <Button variant="ghost" className="text-gray-700 hover:text-blue-600">
                <Search className="h-4 w-4 mr-2" />
                Buscar Vuelos
              </Button>
              <Button variant="ghost" className="text-gray-700 hover:text-blue-600">
                <Users className="h-4 w-4 mr-2" />
                Pasajeros
              </Button>
              <Button variant="ghost" className="text-gray-700 hover:text-blue-600">
                <Calendar className="h-4 w-4 mr-2" />
                Reservas
              </Button>
              <Button variant="ghost" className="text-gray-700 hover:text-blue-600">
                <BarChart3 className="h-4 w-4 mr-2" />
                Reportes
              </Button>
            </nav>
            <Button className="bg-orange-500 hover:bg-orange-600 text-white">
              <Plus className="h-4 w-4 mr-2" />
              Nueva Reserva
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Gestión Integral de Aerolínea</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Sistema completo para la administración de vuelos, reservas, pasajeros y reportes. Optimiza las operaciones
            de tu aerolínea con nuestra plataforma moderna.
          </p>
        </div>

        {/* Estadísticas */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <Card className="bg-white shadow-sm hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Vuelos Hoy</p>
                  <p className="text-3xl font-bold text-blue-600">{estadisticas.vuelosHoy}</p>
                </div>
                <div className="bg-blue-100 p-3 rounded-full">
                  <Plane className="h-6 w-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-sm hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Pasajeros Total</p>
                  <p className="text-3xl font-bold text-green-600">{estadisticas.pasajerosTotal.toLocaleString()}</p>
                </div>
                <div className="bg-green-100 p-3 rounded-full">
                  <Users className="h-6 w-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-sm hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Reservas Activas</p>
                  <p className="text-3xl font-bold text-orange-600">{estadisticas.reservasActivas}</p>
                </div>
                <div className="bg-orange-100 p-3 rounded-full">
                  <Calendar className="h-6 w-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-sm hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Ocupación Promedio</p>
                  <p className="text-3xl font-bold text-purple-600">{estadisticas.ocupacionPromedio}%</p>
                </div>
                <div className="bg-purple-100 p-3 rounded-full">
                  <BarChart3 className="h-6 w-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Búsqueda Rápida */}
        <Card className="mb-12 bg-white shadow-sm">
          <CardHeader>
            <CardTitle className="flex items-center text-gray-900">
              <Search className="h-5 w-5 mr-2 text-blue-600" />
              Búsqueda Rápida de Vuelos
            </CardTitle>
            <CardDescription>Encuentra vuelos disponibles por origen, destino y fecha</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="space-y-2">
                <Label htmlFor="origen">Origen</Label>
                <Input
                  id="origen"
                  placeholder="Ciudad de origen"
                  value={busqueda.origen}
                  onChange={(e) => setBusqueda({ ...busqueda, origen: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="destino">Destino</Label>
                <Input
                  id="destino"
                  placeholder="Ciudad de destino"
                  value={busqueda.destino}
                  onChange={(e) => setBusqueda({ ...busqueda, destino: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="fecha">Fecha</Label>
                <Input
                  id="fecha"
                  type="date"
                  value={busqueda.fecha}
                  onChange={(e) => setBusqueda({ ...busqueda, fecha: e.target.value })}
                />
              </div>
              <div className="flex items-end">
                <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
                  <Search className="h-4 w-4 mr-2" />
                  Buscar Vuelos
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Vuelos Destacados */}
        <Card className="bg-white shadow-sm">
          <CardHeader>
            <CardTitle className="flex items-center text-gray-900">
              <Star className="h-5 w-5 mr-2 text-orange-500" />
              Vuelos Destacados
            </CardTitle>
            <CardDescription>Vuelos más populares y con mayor disponibilidad</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {vuelosDestacados.map((vuelo) => (
                <div key={vuelo.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-6">
                      <div className="text-center">
                        <div className="flex items-center space-x-2 mb-1">
                          <MapPin className="h-4 w-4 text-gray-500" />
                          <span className="font-semibold text-gray-900">{vuelo.origen}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Clock className="h-4 w-4 text-gray-500" />
                          <span className="text-sm text-gray-600">{vuelo.hora}</span>
                        </div>
                      </div>

                      <div className="flex items-center">
                        <div className="w-8 h-px bg-gray-300"></div>
                        <Plane className="h-4 w-4 text-blue-600 mx-2" />
                        <div className="w-8 h-px bg-gray-300"></div>
                      </div>

                      <div className="text-center">
                        <div className="flex items-center space-x-2 mb-1">
                          <MapPin className="h-4 w-4 text-gray-500" />
                          <span className="font-semibold text-gray-900">{vuelo.destino}</span>
                        </div>
                        <div className="text-sm text-gray-600">{vuelo.fecha}</div>
                      </div>
                    </div>

                    <div className="text-right space-y-2">
                      <div className="text-2xl font-bold text-blue-600">€{vuelo.precio}</div>
                      <div className="flex items-center space-x-2">
                        <Badge variant={vuelo.estado === "Programado" ? "default" : "secondary"}>{vuelo.estado}</Badge>
                        <span className="text-sm text-gray-600">
                          {vuelo.disponibles}/{vuelo.total} asientos
                        </span>
                      </div>
                      <Button size="sm" className="bg-orange-500 hover:bg-orange-600 text-white">
                        Reservar
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="bg-blue-600 p-2 rounded-lg">
                  <Plane className="h-6 w-6 text-white" />
                </div>
                <span className="text-xl font-bold">AeroGestión</span>
              </div>
              <p className="text-gray-400">
                Sistema integral de gestión de aerolínea para optimizar operaciones y mejorar la experiencia del
                cliente.
              </p>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Funcionalidades</h3>
              <ul className="space-y-2 text-gray-400">
                <li>Gestión de Vuelos</li>
                <li>Reservas Online</li>
                <li>Control de Pasajeros</li>
                <li>Reportes y Analytics</li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Soporte</h3>
              <ul className="space-y-2 text-gray-400">
                <li>Documentación</li>
                <li>Centro de Ayuda</li>
                <li>Contacto Técnico</li>
                <li>Actualizaciones</li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Contacto</h3>
              <ul className="space-y-2 text-gray-400">
                <li>soporte@aerogestion.com</li>
                <li>+34 900 123 456</li>
                <li>Madrid, España</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 AeroGestión. Sistema de Gestión de Aerolínea. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
