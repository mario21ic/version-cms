<?php
define('_JEXEC', 'xD');
require $argv[1]."/version.php";
$jversion = new JVersion;
echo json_encode($jversion->getShortVersion());
