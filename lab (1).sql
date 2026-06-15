-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-06-2026 a las 00:32:42
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `lab`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `edificios`
--

CREATE TABLE `edificios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `edificios`
--

INSERT INTO `edificios` (`id`, `nombre`, `direccion`, `telefono`) VALUES
(1, 'lasin', 'monoblock central', '12345678'),
(2, 'Informática Central', 'Av. Principal # 100, Campus Central', '71234567');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipos`
--

CREATE TABLE `equipos` (
  `id` int(11) NOT NULL,
  `codigo` varchar(30) NOT NULL,
  `laboratorio_id` int(11) NOT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'operativo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `equipos`
--

INSERT INTO `equipos` (`id`, `codigo`, `laboratorio_id`, `tipo`, `marca`, `modelo`, `estado`) VALUES
(1, 'PC-101-01', 1, 'Computadora', 'Dell', 'OptiPlex 7090', 'operativo'),
(2, 'PC-101-02', 1, 'Computadora', 'HP', 'EliteBook', 'operativo'),
(3, 'PC-103-01', 3, 'Computadora', 'Lenovo', 'ThinkCentre', 'operativo'),
(7, 'PC-LASIN-101-01', 2, 'Computadora', 'Dell', 'OptiPlex', 'operativo'),
(8, 'PC-LASIN-101-02', 2, 'Computadora', 'HP', 'EliteBook', 'operativo'),
(9, 'PC-LASIN-102-01', 2, 'Computadora', 'Lenovo', 'ThinkCentre', 'mantenimiento');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidencias`
--

CREATE TABLE `incidencias` (
  `id` int(11) NOT NULL,
  `laboratorio_id` int(11) NOT NULL,
  `equipo_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `descripcion` text NOT NULL,
  `prioridad` varchar(20) DEFAULT 'media',
  `estado` varchar(20) DEFAULT 'reportada',
  `fecha_reporte` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `incidencias`
--

INSERT INTO `incidencias` (`id`, `laboratorio_id`, `equipo_id`, `usuario_id`, `tipo`, `descripcion`, `prioridad`, `estado`, `fecha_reporte`) VALUES
(1, 1, 2, 3, 'hardware', 'El teclado no funciona', NULL, 'resuelta', '2026-06-15 13:08:28'),
(7, 1, 1, 5, 'software', 'sdsgsgs', 'media', 'reportada', '2026-06-15 18:20:53');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `laboratorios`
--

CREATE TABLE `laboratorios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `piso_id` int(11) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `num_equipos` int(11) DEFAULT 0,
  `especialidad` varchar(100) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'disponible'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `laboratorios`
--

INSERT INTO `laboratorios` (`id`, `nombre`, `piso_id`, `capacidad`, `num_equipos`, `especialidad`, `estado`) VALUES
(1, 'Lab-101 (Redes)', 1, 30, 30, 'Redes y Comunicaciones', 'disponible'),
(2, 'Lab-102 (Hardware)', 1, 25, 25, 'Mantenimiento de Hardware', 'disponible'),
(3, 'Lab-103 (Programación)', 1, 35, 35, 'Programación Avanzada', 'disponible'),
(4, 'Lab-104 (Bases de Datos)', 1, 28, 28, 'Administración de BD', 'disponible'),
(5, 'Lab-105 (Seguridad)', 1, 20, 20, 'Seguridad Informática', 'disponible'),
(6, 'Lab-201 (IA)', 2, 40, 40, 'Inteligencia Artificial', 'disponible'),
(7, 'Lab-202 (Web)', 2, 32, 32, 'Desarrollo Web', 'disponible'),
(8, 'Lab-203 (Multimedia)', 3, 25, 25, 'Edición Multimedia', 'disponible'),
(10, 'redes ', 2, 35, 35, 'connexion a redes ', 'disponible');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pisos`
--

CREATE TABLE `pisos` (
  `id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `edificio_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pisos`
--

INSERT INTO `pisos` (`id`, `numero`, `edificio_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `laboratorio_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `motivo` varchar(200) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'pendiente',
  `aprobado_por` int(11) DEFAULT NULL,
  `fecha_aprobacion` datetime DEFAULT NULL,
  `comentario_admin` varchar(200) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id`, `laboratorio_id`, `usuario_id`, `fecha`, `hora_inicio`, `hora_fin`, `motivo`, `estado`, `aprobado_por`, `fecha_aprobacion`, `comentario_admin`, `created_at`) VALUES
(1, 3, 2, '2026-06-15', '08:00:00', '10:00:00', 'Clase de Programación Avanzada', 'aprobada', 1, '2026-06-15 09:08:11', NULL, '2026-06-15 13:08:11'),
(2, 1, 3, '2026-06-16', '14:00:00', '16:00:00', 'Práctica de redes', 'pendiente', NULL, NULL, NULL, '2026-06-15 13:08:11'),
(6, 1, 5, '2026-06-15', '08:00:00', '18:00:00', 'auxiliatura', 'pendiente', NULL, NULL, NULL, '2026-06-15 18:10:09');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rol` enum('admin','docente','estudiante') NOT NULL,
  `carrera` varchar(100) DEFAULT NULL,
  `departamento` varchar(100) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `password` varchar(200) NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `ultimo_acceso` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `codigo`, `nombre`, `email`, `rol`, `carrera`, `departamento`, `telefono`, `password`, `activo`, `ultimo_acceso`, `created_at`) VALUES
(1, 'ADMIN001', 'Administrador', 'admin@lab.com', 'admin', NULL, NULL, '71234567', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTQvT8Zq6GgE2a', 1, NULL, '2026-06-15 13:07:42'),
(2, 'DOC001', 'Dr. Juan Pérez', 'jperez@universidad.edu', 'docente', NULL, 'Informática', '71234568', '$2b$12$R9hX6kLmN8pQrT3uVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZ0123456', 1, NULL, '2026-06-15 13:07:42'),
(3, '20240001', 'Carlos Gómez', 'cgomez@estudiante.edu', 'estudiante', 'Ingeniería Informática', NULL, '71234569', '$2b$12$S7tU8vW9xYzAbCdEfGhIjKlMnOoPqRStUvWxYz1234567890ABCDE', 1, NULL, '2026-06-15 13:07:42'),
(4, 'ADMIN_NUEVO', 'Administrador Nuevo', 'adminnuevo@lab.com', 'admin', NULL, NULL, '70000000', '$2b$12$9Bvb61UhAnMxAvLIsaUzJenWbAsyPxAu8KhoofAyc6MUsybURbZrG', 1, NULL, '2026-06-15 13:47:47'),
(5, 'EST12', 'Alejandra Fanny Quispe Condori', 'quuspecondorialejandrafanny@gmail.com', 'estudiante', 'infroamtica desallollo de sofware', NULL, '74279901', '$2b$12$q0Q1GbjeKcHEa4Phcp0DG.1VA4dJpx6OTQrYIFA.k8LsJItyXxL5a', 1, NULL, '2026-06-15 17:38:14');

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_disponibilidad`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_disponibilidad` (
`id` int(11)
,`nombre` varchar(50)
,`capacidad` int(11)
,`num_equipos` int(11)
,`especialidad` varchar(100)
,`reservas_hoy` bigint(21)
);

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_disponibilidad`
--
DROP TABLE IF EXISTS `vista_disponibilidad`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_disponibilidad`  AS SELECT `l`.`id` AS `id`, `l`.`nombre` AS `nombre`, `l`.`capacidad` AS `capacidad`, `l`.`num_equipos` AS `num_equipos`, `l`.`especialidad` AS `especialidad`, (select count(0) from `reservas` `r` where `r`.`laboratorio_id` = `l`.`id` and `r`.`fecha` = curdate() and `r`.`estado` in ('aprobada','pendiente')) AS `reservas_hoy` FROM `laboratorios` AS `l` ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `edificios`
--
ALTER TABLE `edificios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`),
  ADD KEY `laboratorio_id` (`laboratorio_id`);

--
-- Indices de la tabla `incidencias`
--
ALTER TABLE `incidencias`
  ADD PRIMARY KEY (`id`),
  ADD KEY `laboratorio_id` (`laboratorio_id`),
  ADD KEY `equipo_id` (`equipo_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `laboratorios`
--
ALTER TABLE `laboratorios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `piso_id` (`piso_id`);

--
-- Indices de la tabla `pisos`
--
ALTER TABLE `pisos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `edificio_id` (`edificio_id`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `laboratorio_id` (`laboratorio_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `aprobado_por` (`aprobado_por`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `edificios`
--
ALTER TABLE `edificios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `equipos`
--
ALTER TABLE `equipos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `incidencias`
--
ALTER TABLE `incidencias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `laboratorios`
--
ALTER TABLE `laboratorios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `pisos`
--
ALTER TABLE `pisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD CONSTRAINT `equipos_ibfk_1` FOREIGN KEY (`laboratorio_id`) REFERENCES `laboratorios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `incidencias`
--
ALTER TABLE `incidencias`
  ADD CONSTRAINT `incidencias_ibfk_1` FOREIGN KEY (`laboratorio_id`) REFERENCES `laboratorios` (`id`),
  ADD CONSTRAINT `incidencias_ibfk_2` FOREIGN KEY (`equipo_id`) REFERENCES `equipos` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `incidencias_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `laboratorios`
--
ALTER TABLE `laboratorios`
  ADD CONSTRAINT `laboratorios_ibfk_1` FOREIGN KEY (`piso_id`) REFERENCES `pisos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pisos`
--
ALTER TABLE `pisos`
  ADD CONSTRAINT `pisos_ibfk_1` FOREIGN KEY (`edificio_id`) REFERENCES `edificios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`laboratorio_id`) REFERENCES `laboratorios` (`id`),
  ADD CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `reservas_ibfk_3` FOREIGN KEY (`aprobado_por`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
