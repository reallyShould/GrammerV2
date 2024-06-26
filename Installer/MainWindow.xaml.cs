﻿using Microsoft.Win32.TaskScheduler;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Windows;
using WinForms = System.Windows.Forms;

namespace Installer
{
    public partial class MainWindow : Window
    {
        private string defaultDir = Directory.GetCurrentDirectory();
        private string grammerURL = "https://github.com/reallyShould/GrammerV2/releases/download/Last/GrammerV2.exe";
        private string grammerStart;
        private bool installed = false;
        private string taskName = "GrammerV2";
        static private string user_name = Environment.UserName;
        private string grammerPathDefault = $"C:\\Users\\{user_name}\\AppData\\Roaming\\GrammerV2";
        private string grammerPath;


        public MainWindow()
        {
            grammerPath = grammerPathDefault;
            InitializeComponent();
            Init();
        }
        private void Init()
        {
            grammerStart = $"{grammerPath}\\GrammerV2.exe";

            if (File.Exists(grammerStart))
                installed = true;
            else
                installed = false;

            PathTextBoxXAML.Text = grammerPath;

            if (installed)
            {
                InstallButtonXAML.IsEnabled = false;
                DeleteButtonXAML.IsEnabled = true;
            }
            else
            {
                InstallButtonXAML.IsEnabled = true;
                DeleteButtonXAML.IsEnabled = false;
            }
        }

        private void SelectButtonXAML_Click(object sender, RoutedEventArgs e)
        {
            WinForms.FolderBrowserDialog dialog = new WinForms.FolderBrowserDialog();
            dialog.ShowDialog();
            if (dialog.SelectedPath != "")
            {
                grammerPath = dialog.SelectedPath;
                PathTextBoxXAML.Text = grammerPath;
            }
            Init();
        }

        private void InstallButtonXAML_Click(object sender, RoutedEventArgs e)
        {
            if (!Directory.Exists(grammerPath))
            {
                Directory.CreateDirectory(grammerPath);
            }
            using (var client = new WebClient())
            {
                client.DownloadFile(grammerURL, grammerStart);
            }
            StreamWriter writer = new StreamWriter($"{grammerPath}\\token.txt");
            writer.Write(TokenTextBoxXAML.Text);
            writer.Close();

            StreamWriter adm = new StreamWriter($"{grammerPath}\\admin.txt");
            adm.Write(IDTextBoxXAML.Text);
            adm.Close();

            if (AutorunCheckerXAML.IsChecked == true)
            {
                autorun();
            }

            defaultDir = Directory.GetCurrentDirectory();
            Directory.SetCurrentDirectory(grammerPath);
            Process.Start(grammerStart);
            Directory.SetCurrentDirectory(defaultDir);
            Init();
        }

        private void DeleteButtonXAML_Click(object sender, RoutedEventArgs e)
        {
            Kill("GrammerV2");
            System.Threading.Thread.Sleep(3000);
            Delete(grammerPath);
            try
            {
                using (TaskService ts = new TaskService())
                {
                    ts.RootFolder.DeleteTask($"{taskName}");
                }
            }
            catch (Exception ex) { System.Windows.MessageBox.Show(ex.Message); }
            Init();
        }

        private void autorun()
        {
            try
            {
                using (TaskService ts = new TaskService())
                {
                    TaskDefinition td = ts.NewTask();
                    td.Actions.Add(new ExecAction(grammerStart, workingDirectory: grammerPath));
                    td.Triggers.Add(new LogonTrigger { UserId = user_name, Delay = TimeSpan.FromSeconds(30) });
                    ts.RootFolder.RegisterTaskDefinition($@"{taskName}", td);
                }
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show(ex.Message);
            }
        }

        public void Kill(string name)
        {
            try
            {
                foreach (Process proc in Process.GetProcessesByName(name))
                {
                    proc.Kill();
                }
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show(ex.Message);
            }
        }

        public void Delete(string dir)
        {
            try
            {
                foreach (var file in Directory.GetFiles(dir))
                {
                    try
                    {
                        File.Delete(file);
                    }
                    catch (Exception ex) { System.Windows.MessageBox.Show(ex.Message); }
                }

                foreach (var subdir in Directory.GetDirectories(dir))
                {
                    Delete(subdir);
                }

                try
                {
                    Directory.Delete(dir);
                }
                catch (Exception ex) { System.Windows.MessageBox.Show(ex.Message); }
            }
            catch (Exception ex) { System.Windows.MessageBox.Show(ex.Message); }
        }
    }
}
