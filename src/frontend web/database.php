<?php
/**
 * Create an Oracle connection from environment variables.
 *
 * Required: ORACLE_DB_USER and ORACLE_DB_PASSWORD
 * Optional: ORACLE_DB_DSN (defaults to localhost/XE)
 */
function createDatabaseConnection()
{
    $username = getenv('ORACLE_DB_USER');
    $password = getenv('ORACLE_DB_PASSWORD');
    $dsn = getenv('ORACLE_DB_DSN') ?: 'localhost/XE';

    if (!$username || !$password) {
        die('Database configuration is missing. Set ORACLE_DB_USER and ORACLE_DB_PASSWORD.');
    }

    $connection = oci_connect($username, $password, $dsn);
    if (!$connection) {
        $error = oci_error();
        $message = isset($error['message']) ? $error['message'] : 'Unknown Oracle connection error';
        die('Could not connect to Oracle: ' . htmlspecialchars($message, ENT_QUOTES, 'UTF-8'));
    }

    return $connection;
}
