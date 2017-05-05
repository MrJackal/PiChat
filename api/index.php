<?php
session_start();
require 'Slim/Slim.php';

\Slim\Slim::registerAutoloader();

$app = new \Slim\Slim();

$app->group('/api', function() use($app){
    $app->group('/commands', function() use($app){
        $app->get('/help', function() use($app){
            $commands = array(
                array(
                    "name"=>"help",
                    "desc"=>"A list of all commands.",
                    "cli_cmd"=>"get_help"
                )
            );
            echo json_encode($commands);
        });

        $app->get('/all', function() use($app){
            $commands = array(
                array(
                    "name"=>"list",
                    "desc"=>"Will return all online users.",
                    "usage"=>"!list",
                    "srv_cmd"=>"get_userlist"
                ),
                array(
                    "name"=>"quit",
                    "desc"=>"This will disconnect your from the server.",
                    "usage"=>"!quit",
                    "srv_cmd"=>"user_disconnect"
                ),
                array(
                    "name"=>"msg",
                    "desc"=>"Send a private message to the specified person",
                    "usage"=>"!msg [user]",
                    "srv_cmd"=>"send_privatemessage"
                ),
                array(
                    "name"=>"ban",
                    "desc"=>"Ban the specified person from the server or Ban them for a certain time e.g. 1m, 3h, 4d, 5w, 6M, 7Y.",
                    "usage"=>"!ban [user] {time}",
                    "srv_cmd"=>"user_ban"
                ),
                array(
                    "name"=>"kick",
                    "desc"=>"Kick the specified person from the server.",
                    "usage"=>"!kick [user]",
                    "srv_cmd"=>"user_kick"
                ),
                array(
                    "name"=>"mute",
                    "desc"=>"Mute the specified person or Mute then for a certain time e.g. 1m, 3h, 4d, 5w, 6M, 7Y.",
                    "usage"=>"!mute [user] {time}",
                    "srv_cmd"=>"user_mute"
                )
            );
            echo json_encode($commands);
        });
    });
});

$app->run();
