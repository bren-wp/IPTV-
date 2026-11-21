// IPTV+ portable Windows host. Contains the COMPLETE Flutter runner folder.
// No installer; unpacks into a new temporary directory and removes it on exit.
// Original clubTivi Flutter binaries stay LGPL/Apache/etc according to dependencies.
using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Windows.Forms;

internal static class Program
{
    [STAThread]
    private static int Main()
    {
        var path = Path.Combine(Path.GetTempPath(), "IPTVPlus-Portable-" + Guid.NewGuid().ToString("N"));
        try
        {
            Directory.CreateDirectory(path);
            using (Stream archiveBytes = Assembly.GetExecutingAssembly()
                    .GetManifestResourceStream("FlutterBundle")
                    ?? throw new FileNotFoundException("Embedded Flutter payload missing"))
            using (var archive = new ZipArchive(archiveBytes, ZipArchiveMode.Read))
            {
                foreach (var entry in archive.Entries)
                {
                    string target = Path.GetFullPath(Path.Combine(path, entry.FullName));
                    string root = Path.GetFullPath(path) + Path.DirectorySeparatorChar;
                    if (!target.StartsWith(root, StringComparison.OrdinalIgnoreCase))
                        throw new InvalidDataException("Unsafe Flutter bundle path");
                    if (string.IsNullOrEmpty(entry.Name))
                    {
                        Directory.CreateDirectory(target);
                        continue;
                    }
                    Directory.CreateDirectory(Path.GetDirectoryName(target)!);
                    entry.ExtractToFile(target, overwrite: false);
                }
            }
            string executable = Path.Combine(path, "iptvplus.exe");
            if (!File.Exists(executable))
                throw new FileNotFoundException("Branded Flutter binary is missing", executable);
            using var process = Process.Start(new ProcessStartInfo(executable)
            {
                WorkingDirectory = path,
                UseShellExecute = true
            }) ?? throw new InvalidOperationException("Unable to start IPTV+");
            process.WaitForExit();
            return process.ExitCode;
        }
        catch (Exception ex)
        {
            MessageBox.Show("IPTV+ Portable nije moguće pokrenuti.\n" + ex.Message,
                "IPTV+ Portable", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 1;
        }
        finally
        {
            try { Directory.Delete(path, true); }
            catch (IOException) { /* Windows may still have locked files */ }
            catch (UnauthorizedAccessException) { }
        }
    }
}
