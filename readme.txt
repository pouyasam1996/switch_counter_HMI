sudo systemctl daemon-reload
sudo systemctl restart main_app.service


sudo systemctl stop    main_app.service     # stop listener and any running job
sudo systemctl start   main_app.service     # start listener again
sudo systemctl restart main_app.service     # quick restart
sudo systemctl status  main_app.service     # health check




python /home/pnppharma/Desktop/switch_detector_effytect/scripts/main.py