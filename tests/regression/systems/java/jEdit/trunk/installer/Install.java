/*
 * Install.java - Main class of the installer
 *
 * Originally written by Slava Pestov for the jEdit installer project. This work
 * has been placed into the public domain. You may use this work in any way and
 * for any purpose you wish.
 *
 * THIS SOFTWARE IS PROVIDED AS-IS WITHOUT WARRANTY OF ANY KIND, NOT EVEN THE
 * IMPLIED WARRANTY OF MERCHANTABILITY. THE AUTHOR OF THIS SOFTWARE, ASSUMES
 * _NO_ RESPONSIBILITY FOR ANY CONSEQUENCE RESULTING FROM THE USE, MODIFICATION,
 * OR REDISTRIBUTION OF THIS SOFTWARE.
 */

package installer;

import javax.swing.plaf.metal.*;
import javax.swing.*;
import java.io.*;
import java.util.Properties;
import java.security.*;
import java.net.URL;

public class Install
{
	/**
	 * detects wether the installer is running from a path
	 * containing exclamation marks.
	 * This has been reported as a cause of failure on Linux and MS Windows :
	 * see bug #2065330 - Installer doesn't run on dir having ! as last char in name.
	 */
	public static boolean isRunningFromExclam()
	{
		Class me = Install.class;
		ProtectionDomain domaine = me.getProtectionDomain();
		CodeSource source = domaine.getCodeSource();
		URL mySource = source.getLocation();
		// In fact the check is more restrictive than required :
		// a problem occurs only when the ! is at the end of directory
		return mySource.toString().contains("!");		
	}
	
	public static void main(String[] args)
	{
		
		String javaVersion = System.getProperty("java.version");
		if(javaVersion.compareTo("1.5") < 0)
		{
			String message = "You are running Java version "
					+ javaVersion + " from "+System.getProperty("java.vendor")+".\n"
					+"This installer requires Java 1.5 or later.";
			if(args.length == 0)
			{
				JOptionPane.showMessageDialog(null,
					message,
					"jEdit installer...", JOptionPane.ERROR_MESSAGE); 
			}
			else
			{
				System.err.println(message);
			}
			System.exit(1);
		}

		if(isRunningFromExclam())
		{
			String message = "You are running the installer"
					+"\nfrom a directory with exclamation mark in it."
					+ "\nIt is a known cause of failure of the installer,"
					+ "\nplease move the installer somewhere else and run it again.";
			if(args.length == 0)
			{
				JOptionPane.showMessageDialog(null,
					message,
					"jEdit installer...", JOptionPane.ERROR_MESSAGE); 
			}
			else
			{
				System.err.println(message);
			}
			System.exit(1);
		}

		if(args.length == 0)
			new SwingInstall();
		else if(args.length == 1 && args[0].equals("text"))
			new ConsoleInstall();
		else if(args.length >= 2 && args[0].equals("auto"))
			new NonInteractiveInstall(args);
		else
		{
			System.err.println("Usage:");
			System.err.println("java -jar <installer JAR>");
			System.err.println("java -jar <installer JAR> text");
			System.err.println("java -jar <installer JAR> auto"
				+ " <install dir> [unix-script=<dir>] [unix-man=<dir>]");
			System.err.println("text parameter starts installer in text-only mode.");
			System.err.println("auto parameter starts installer in non-interactive mode.");
		}
	}

	public Install()
	{
		props = new Properties();
		try
		{
			InputStream in = getClass().getResourceAsStream("/installer/install.props");
			props.load(in);
			in.close();
		}
		catch(IOException io)
		{
			System.err.println("Error loading 'install.props':");
			io.printStackTrace();
		}

		buf = new byte[32768];
	}

	public String getProperty(String name)
	{
		return props.getProperty(name);
	}

	public int getIntegerProperty(String name)
	{
		try
		{
			return Integer.parseInt(props.getProperty(name));
		}
		catch(Exception e)
		{
			return -1;
		}
	}

	public void copy(InputStream in, String outfile, Progress progress)
		throws IOException
	{
		File outFile = new File(outfile);

		OperatingSystem.getOperatingSystem().mkdirs(outFile.getParent());

		BufferedOutputStream out = new BufferedOutputStream(
			new FileOutputStream(outFile));

		int count;

		for(;;)
		{
			count = in.read(buf,0,Math.min(in.available(),buf.length));
			if(count == -1 || count == 0)
				break;

			out.write(buf,0,count);
			if(progress != null)
				progress.advance(count);
		}

		//in.close();
		out.close();
	}

	// private members
	private Properties props;
	private byte[] buf;
}
